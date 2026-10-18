#!/usr/bin/env python3
"""Build the review paper DOCX from paper_part{1,2,3}.py blocks.
Citation placeholders [[doi]] resolve to numbered [n] refs in first-appearance order;
consecutive citations merge into ranges [n-n2]."""
import os
import re, json, sys
from collections import Counter
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paper_part1, paper_part2, paper_part3

CORPUS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'corpus/papers_final.json')))
CONF = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'corpus/conference_verified.json')))
EXT = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'corpus/external_verified.json')))
STD_REFS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'corpus/standards_refs.json')))
BY_DOI = {r['doi']: r for r in CORPUS}
BY_DOI.update({r['doi']: r for r in CONF})
BY_DOI.update({r['doi']: r for r in EXT})
BY_DOI.update({r['doi']: r for r in STD_REFS})

BLOCKS = (paper_part1.BLOCKS + paper_part2.BLOCKS + paper_part3.BLOCKS)
TABLES = {'table1': paper_part3.TABLE1, 'TABLE2': paper_part3.TABLE2,
          'TABLE3': paper_part3.TABLE3, 'TABLE_METH': paper_part3.TABLE_METH,
          'TABLE_DATASETS': paper_part3.TABLE_DATASETS, 'TABLE_VALID': paper_part3.TABLE_VALID,
          'TABLE_GAPS': paper_part3.TABLE_GAPS,
          'TABLE_FLEET': paper_part3.TABLE_FLEET,
          'TABLE_CONF': paper_part3.TABLE_CONF,
          'TABLE_LLM': paper_part3.TABLE_LLM,
          'TABLE_STD': paper_part3.TABLE_STD,
          'TABLE_POSITION': paper_part3.TABLE_POSITION,
          'TABLE_CHECKLIST': paper_part3.TABLE_CHECKLIST}
TITLE = paper_part1.TITLE
AUTHORS = paper_part1.AUTHOR_LINES
ABSTRACT = paper_part1.ABSTRACT
KEYWORDS = paper_part1.KEYWORDS

CITE_RE = re.compile(r'\[\[([^\]]+)\]\]')

# ---------- resolve citation numbering in document order ----------
order = []          # DOIs in first-appearance order
num = {}            # doi -> 1-based number
def note(doi):
    if doi not in num:
        num[doi] = len(order) + 1
        order.append(doi)

for kind, *rest in BLOCKS:
    if kind in ('p', 'decl') and rest[0]:
        for m in CITE_RE.finditer(rest[0]):
            note(m.group(1))
    elif kind == 'fig':
        caption = rest[1]
        for m in CITE_RE.finditer(caption):
            note(m.group(1))
    elif kind == 'tbl':
        t = TABLES.get(rest[0])
        if t and isinstance(t.get('rows'), list):
            for row in t['rows']:
                for cell in row:
                    for m in CITE_RE.finditer(cell):
                        note(m.group(1))

# any corpus papers never cited -> append at end (should be none ideally)
uncited = [r['doi'] for r in CORPUS if r['doi'] not in num]
print('cited in order:', len(order), '| uncited corpus papers:', len(uncited))
for d in uncited:
    print('  UNCITED:', d, BY_DOI[d]['title_cr'][:60])

def fix(s):
    return s.replace('&amp;', '&').replace('fast-chaging', 'fast-charging')

def ref_text(doi):
    r = BY_DOI[doi]
    auth = r['authors'] or 'Anonymous'
    auth = re.sub(r'; et al\.$', ', et al.', auth)
    auth = auth.replace(';', ',')
    t = fix(r['title_cr']).rstrip('.')
    jr = fix(r['journal'])
    vol = r['volume'] or ''
    pg = r['page'] or (f"Art. no. {r['article_number']}" if r['article_number'] else '')
    yr = r['year']
    s = f'{auth}, \u201c{t},\u201d {jr}'
    if vol:
        s += f', vol. {vol}'
    if pg:
        s += f', {pg}'
    if doi.startswith('std:'):
        s += f', {yr}.'
        if r.get('xref'):
            s += ' ' + str(r['xref']).rstrip('.') + '.'
        if r.get('url'):
            s += f' [Online]. Available: {r["url"]}'
    else:
        s += f', {yr}, doi: {doi}.'
    if doi in REF_NOTES:
        s += ' ' + REF_NOTES[doi]
    return s

# One-line disclosure notes appended to specific reference entries (reviewer request):
# the RFID-journal entry is a battery SOC estimation study published in an
# identification-technology venue; the note states why it is retained.
REF_NOTES = {
    '10.1109/jrfid.2022.3211841': (
        'Note: lithium-ion battery state-of-charge estimation study published in an '
        'identification-technology venue (IEEE Journal of Radio Frequency Identification); '
        'retained on DOI-verified method content, venue notwithstanding.'),
}

# ---------- DOCX setup ----------
doc = Document()
# page geometry: US Letter, 1-inch margins, single column (default)
sec = doc.sections[0]
sec.page_width, sec.page_height = Inches(8.5), Inches(11)
for m in ('top_margin', 'bottom_margin', 'left_margin', 'right_margin'):
    setattr(sec, m, Inches(1))

style = doc.styles['Normal']
style.font.name = 'Times New Roman'
style.font.size = Pt(10)
style.element.rPr.rFonts.set(qn('w:eastAsia'), 'Times New Roman')
pf = style.paragraph_format
pf.space_after = Pt(8)
pf.line_spacing = 1.15
pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

ITAL_RE = re.compile(r'\*([^*\n]+)\*')

def add_runs(p, text, size=10, bold=False, italic=False):
    """Add runs to paragraph, honoring *italic* spans."""
    pos = 0
    for m in ITAL_RE.finditer(text):
        if m.start() > pos:
            r = p.add_run(text[pos:m.start()])
            r.font.name = 'Times New Roman'; r.font.size = Pt(size)
            r.bold = bold; r.italic = italic
        r = p.add_run(m.group(1))
        r.font.name = 'Times New Roman'; r.font.size = Pt(size)
        r.bold = bold; r.italic = True
        pos = m.end()
    if pos < len(text):
        r = p.add_run(text[pos:])
        r.font.name = 'Times New Roman'; r.font.size = Pt(size)
        r.bold = bold; r.italic = italic

def para(text='', size=10, bold=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY,
         space_after=8, italic=False, color=None):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    if text:
        add_runs(p, text, size=size, bold=bold, italic=italic)
    return p

def rich_cite(p, text, size=10):
    """Append text to paragraph with [[doi]] -> [n] resolution, merging runs."""
    pos = 0
    out = []
    last_end = 0
    for m in CITE_RE.finditer(text):
        out.append(('t', text[last_end:m.start()]))
        out.append(('c', num[m.group(1)]))
        last_end = m.end()
    out.append(('t', text[last_end:]))
    # merge consecutive citations into ranges
    merged = []
    pending = []
    for kind, val in out:
        if kind == 'c':
            pending.append(val)
        else:
            if pending and val.strip():
                merged.append(('c', pending)); pending = []
            if val != '':
                merged.append(('t', val))
    if pending:
        merged.append(('c', pending))
    for kind, val in merged:
        if kind == 't':
            if val:
                add_runs(p, fix(val), size=size)
        else:
            val = sorted(set(val))
            parts, i = [], 0
            while i < len(val):
                j = i
                while j + 1 < len(val) and val[j + 1] == val[j] + 1:
                    j += 1
                if j - i >= 2:
                    parts.append(f'{val[i]}\u2013{val[j]}')
                else:
                    parts.extend(str(x) for x in val[i:j + 1])
                i = j + 1
            r = p.add_run('[' + ', '.join(parts) + ']')
            r.font.name = 'Times New Roman'; r.font.size = Pt(size)
            r.font.superscript = False

def add_table(spec):
    cap = para(fix(spec['caption']), size=9, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=4)
    cap.paragraph_format.keep_with_next = True
    rows = spec['rows']
    if rows == 'AUTO_AREA_YEAR':
        stats = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'corpus/stats.json')))
        ay = stats['area_by_year']
        years = ['2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026']
        rev = Counter(r['area'] for r in CORPUS if r['method'] == 'Review / perspective' or r['valid'] == 'review synthesis')
        rows = []
        for a, m in sorted(ay.items()):
            tot = sum(m.values())
            rv = rev.get(a, 0)
            rows.append([a] + [str(m.get(y, 0)) for y in years] + [str(tot), str(rv), str(tot - rv)])
        total = ['Total'] + [str(sum(int(r[i + 1]) for r in rows)) for i in range(len(years))]
        total += [str(len(CORPUS)), str(sum(rev.values())), str(len(CORPUS) - sum(rev.values()))]
        rows.append(total)
    tbl = doc.add_table(rows=1 + len(rows), cols=len(spec['header']))
    tbl.style = 'Table Grid'
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tblPr = tbl._tbl.tblPr
    layout = OxmlElement('w:tblLayout')
    layout.set(qn('w:type'), 'fixed')
    tblPr.append(layout)
    widths = spec.get('widths')
    if widths:
        grid = tbl._tbl.find(qn('w:tblGrid'))
        for gc, w in zip(grid.findall(qn('w:gridCol')), widths):
            gc.set(qn('w:w'), str(int(w * 1440)))
    def _cant_split(row):
        trPr = row._tr.get_or_add_trPr()
        trPr.append(OxmlElement('w:cantSplit'))
    _cant_split(tbl.rows[0])
    trPr = tbl.rows[0]._tr.get_or_add_trPr()
    trPr.append(OxmlElement('w:tblHeader'))
    for row in tbl.rows[1:]:
        _cant_split(row)
    for j, h in enumerate(spec['header']):
        c = tbl.cell(0, j)
        if widths:
            c.width = Inches(widths[j])
        c.text = ''
        r = c.paragraphs[0].add_run(h)
        r.bold = True; r.font.size = Pt(8.5); r.font.name = 'Times New Roman'
        c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    for i, row in enumerate(rows, 1):
        for j, cell in enumerate(row):
            c = tbl.cell(i, j)
            if widths:
                c.width = Inches(widths[j])
            c.text = ''
            p = c.paragraphs[0]
            text = fix(str(cell))
            for m in CITE_RE.finditer(text):
                note(m.group(1))
            # render with citation resolution
            pos = 0
            for m in CITE_RE.finditer(text):
                if m.start() > pos:
                    add_runs(p, text[pos:m.start()], size=8.5)
                r = p.add_run('[' + str(num[m.group(1)]) + ']')
                r.font.size = Pt(8.5); r.font.name = 'Times New Roman'
                pos = m.end()
            if pos < len(text):
                add_runs(p, text[pos:], size=8.5)
            if j == 0 or len(str(cell)) < 8:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j > 0 and len(str(cell)) < 8 else WD_ALIGN_PARAGRAPH.LEFT
    para('', size=6, space_after=6)

# ---------- assemble ----------
para(TITLE, size=20, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=14)
for name, aff in AUTHORS:
    para(name, size=11, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    para(aff, size=9, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)

para('Abstract', size=10, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=6)
for a in ABSTRACT:
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_after = Pt(8)
    add_runs(p, a, size=10)  # honors *italic* markers (was: literal asterisks)
para('Keywords: ' + KEYWORDS, size=10, italic=True, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=12)

fig_count = 0
for kind, *rest in BLOCKS:
    if kind == 'h1':
        hp = para(rest[0], size=10, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=6)
        hp.paragraph_format.keep_with_next = True
    elif kind == 'h2':
        hp = para(rest[0], size=10, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=4)
        hp.paragraph_format.keep_with_next = True
    elif kind == 'p':
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_after = Pt(8)
        rich_cite(p, rest[0])
    elif kind == 'fig':
        path, caption = rest[0], rest[1]
        fig_w = float(rest[2]) if len(rest) > 2 else 4.9
        fig_count += 1
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run()
        run.add_picture(os.path.join(os.path.dirname(os.path.abspath(__file__)), path), width=Inches(fig_w))
        cp = doc.add_paragraph(); cp.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        cp.paragraph_format.space_after = Pt(10)
        cp.paragraph_format.keep_together = True
        rich_cite_caption(cp, caption) if False else None
        rich_cite(cp, caption, size=9)
    elif kind == 'tbl':
        add_table(TABLES[rest[0]])
    elif kind == 'box':
        title, rows = rest[0], rest[1]
        t = doc.add_table(rows=1, cols=1)
        t.style = 'Table Grid'
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = t.cell(0, 0)
        shd = OxmlElement('w:shd'); shd.set(qn('w:val'), 'clear'); shd.set(qn('w:fill'), 'F2F2F2')
        cell._tc.get_or_add_tcPr().append(shd)
        p0 = cell.paragraphs[0]
        r = p0.add_run(title); r.bold = True; r.font.size = Pt(9.5); r.font.name = 'Times New Roman'
        p0.paragraph_format.space_after = Pt(4)
        for lead, txt in rows:
            pp = cell.add_paragraph(); pp.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            pp.paragraph_format.space_after = Pt(3)
            r1 = pp.add_run(lead + ' '); r1.bold = True; r1.font.size = Pt(9); r1.font.name = 'Times New Roman'
            r2 = pp.add_run(txt); r2.font.size = Pt(9); r2.font.name = 'Times New Roman'
        sp = doc.add_paragraph(); sp.paragraph_format.space_after = Pt(8)
    elif kind == 'decl':
        para('Declarations', size=10, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=6)
        decl = [
         ('Funding', 'The authors received no specific funding for this work.'),
         ('Conflicts of interest', 'The authors declare no competing interests.'),
         ('Author contributions', 'H.T.S. conceived the study, designed and executed the search, screening, and verification pipeline, performed the full-text classification and analysis, coded the released labels, and drafted the manuscript. S.S.I.A. and J.I.C. performed the blind 30-paper re-coding of the reliability study (coders B and C, Section 2.5) before any verification work, and contributed to corpus curation, verification of classifications and counts, and manuscript revision. All authors read and approved the final manuscript.'),
         ('Data availability', 'The complete evidence base is deposited at Zenodo, DOI 10.5281/zenodo.23436202 (deposit of record; the GitHub repository of the same name is a development mirror). The deposit includes: the classified 103-study dataset (papers.csv, papers_final.json) with per-paper citation counts; the 799-record rule-based eligible pool (eligible_corpus.json, pool.csv) with per-record query-theme tags; the record-level screening log (screening_log.csv); the per-paper validation-protocol audit (protocol_audit.csv); the codebook and coding protocol (codebook.md, coding_protocol.md); the locked blind coder sheets, agreement report, itemized disagreements, and hash-tracked reliability log (corpus/reliability/); the conference sensitivity set with all 14 retrieved papers and the pre-stated inclusion rule (conference_sensitivity.csv); the withheld released labels for the reliability sample (gold_labels_30.csv); the label-noise sensitivity script and outputs (sensitivity_label_noise.py/.json); the Crossref verification audit trail (final_audit.json, external_verified.json, conference_verified.json); the seed-study register (seeds.json); the screening statistics (stats.json); the recall audit with its cached Crossref responses (recall_audit.py, recall_audit.json, raw_cache/); the minimum-detectable-effect analysis (power_analysis.py, power_analysis.json); and the abstract-level probes with their codes and rubric (abstract_probe.py, abstract_probe_raw.json, abstract_probe_codes.py, abstract_probe.json). One registry-metadata note: the Crossref record for one reference (DOI 10.1016/j.jechem.2023.03.026) deposits two author names with the given and family fields transposed and the surname \u2018Store\u2019 for \u2018Stroe\u2019; the reference list normalizes them to the published forms (Vilsen, S. B.; Stroe, D. I.), and all other bibliographic metadata is reproduced exactly as deposited.'),
         ('Supplementary material', 'The interpretation rules, the label-noise scenario derivations, the minimum-detectable-effect analysis, the recall-audit construction, and the abstract-level probes are consolidated in Supplementary_Material.pdf (built by build_supplement.py and released with this paper\u2019s repository; the underlying scripts and outputs are part of the same Zenodo deposit, DOI 10.5281/zenodo.23436202).'),
         ('Code availability', 'All search, screening, selection, verification, classification, reliability, sensitivity, statistics, figure-generation, and manuscript-build scripts are included in the same Zenodo deposit (DOI 10.5281/zenodo.23436202), so that every figure and every count in Sections 3 and 3.5 can be regenerated deterministically from the released data.'),
         ('Ethics approval', 'Not applicable. This study did not involve human participants or animals.'),
         ('Consent to participate / for publication', 'Not applicable.'),
         ('Use of artificial intelligence', 'During the preparation of this manuscript the authors used the following tools, each for a stated purpose: an AI language model (GLM, Z.ai) assisted in drafting and adapting the literature-pooling, analysis, and figure-generation scripts; OpenAI ChatGPT, Grammarly, and QuillBot were used for language editing (grammar, readability, and sentence restructuring). No AI tool decided study inclusion, and no AI tool assigned or altered any classification label: all screening decisions and all released labels were made by the authors (Section 2.5 documents who coded what, and the reliability files release the coding evidence). All included references were verified against the Crossref registry by direct DOI resolution, all counts and figures were regenerated programmatically from the released dataset, and the authors reviewed and take full responsibility for the content of the published article.'),
        ]
        for h, b in decl:
            p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.space_after = Pt(4)
            r = p.add_run(h + '. '); r.bold = True; r.font.size = Pt(10); r.font.name = 'Times New Roman'
            r = p.add_run(b); r.font.size = Pt(10); r.font.name = 'Times New Roman'

# ---------- acknowledgment ----------
# Tool-use acknowledgments are consolidated in the single 'Use of artificial intelligence'
# declaration above (merged per review); no separate acknowledgment section is carried.

# ---------- references ----------
para('References', size=10, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=6)
for i, doi in enumerate(order, 1):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.left_indent = Inches(0.25)
    p.paragraph_format.first_line_indent = Inches(-0.25)
    r = p.add_run(f'{i}. '); r.font.size = Pt(9); r.font.name = 'Times New Roman'
    r = p.add_run(ref_text(doi)); r.font.size = Pt(9); r.font.name = 'Times New Roman'

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ML-BMS-Review.docx')
doc.save(out)
print('saved', out)
print('figures:', fig_count, '| references:', len(order), '| corpus size:', len(CORPUS))
