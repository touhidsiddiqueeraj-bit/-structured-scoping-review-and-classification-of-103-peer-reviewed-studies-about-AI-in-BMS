#!/usr/bin/env python3
"""Build the IEEE Transactions submission: IEEEtran LaTeX from the same
paper_part{1,2,3}.py blocks used for the DOCX (single source of truth)."""
import json, re, sys, os

sys.path.insert(0, '/home/touhid/Documents/reviewpaper')
import paper_part1, paper_part2, paper_part3

ROOT = '/home/touhid/Documents/reviewpaper'
OUT_TEX = f'{ROOT}/ieee_submission/tex/mlbms.tex'
FIGDIR = f'{ROOT}/ieee_submission/tex/figs'

CORPUS = json.load(open(f'{ROOT}/corpus/papers_final.json'))
CONF = json.load(open(f'{ROOT}/corpus/conference_verified.json'))
BY_DOI = {r['doi']: r for r in CORPUS}
BY_DOI.update({r['doi']: r for r in CONF})

TABLES = {'table1': paper_part3.TABLE1, 'TABLE2': paper_part3.TABLE2,
          'TABLE3': paper_part3.TABLE3, 'TABLE_METH': paper_part3.TABLE_METH,
          'TABLE_DATASETS': paper_part3.TABLE_DATASETS, 'TABLE_VALID': paper_part3.TABLE_VALID,
          'TABLE_GAPS': paper_part3.TABLE_GAPS, 'TABLE_FLEET': paper_part3.TABLE_FLEET,
          'TABLE_CONF': paper_part3.TABLE_CONF, 'TABLE_LLM': paper_part3.TABLE_LLM,
          'TABLE_CHECKLIST': paper_part3.TABLE_CHECKLIST}

BLOCKS = paper_part1.BLOCKS + paper_part2.BLOCKS + paper_part3.BLOCKS
TITLE = paper_part1.TITLE
AUTHORS = paper_part1.AUTHOR_LINES
ABSTRACT = paper_part1.ABSTRACT
KEYWORDS = paper_part1.KEYWORDS
CITE_RE = re.compile(r'\[\[([^\]]+)\]\]')
ITAL_RE = re.compile(r'\*([^*\n]+)\*')

# ---------- citation numbering (first appearance) ----------
order, num = [], {}
def note(doi):
    if doi not in num:
        num[doi] = len(order) + 1
        order.append(doi)

for kind, *rest in BLOCKS:
    if kind in ('p', 'decl') and rest[0]:
        for m in CITE_RE.finditer(rest[0]):
            note(m.group(1))
    elif kind == 'fig':
        for m in CITE_RE.finditer(rest[1]):
            note(m.group(1))
    elif kind == 'tbl':
        t = TABLES.get(rest[0])
        if t and isinstance(t.get('rows'), list):
            for row in t['rows']:
                for cell in row:
                    for m in CITE_RE.finditer(cell):
                        note(m.group(1))

# ---------- LaTeX helpers ----------
UNI = [('\u2014', '---'), ('\u2013', '--'), ('\u2212', '$-$'), ('\u00d7', '$\\times$'),
       ('\u2248', '$\\approx$'), ('\u2264', '$\\le$'), ('\u2265', '$\\ge$'),
       ('\u00b1', '$\\pm$'), ('\u00b0', '$^\\circ$'), ('\u201c', '``'), ('\u201d', "''"),
       ('\u2018', '`'), ('\u2019', "'"), ('\u2026', '...'), ('\u2192', '$\\to$')]

def esc(t):
    t = t.replace('&amp;', '&').replace('fast-chaging', 'fast-charging')
    t = t.replace('\\', r'\textbackslash{}')
    for ch, rep in [(r'&', r'\&'), (r'%', r'\%'), (r'$', r'\$'), (r'#', r'\#'),
                    (r'_', r'\_'), (r'{', r'\{'), (r'}', r'\}'), (r'~', r'\textasciitilde{}'),
                    (r'\^', r'\textasciicircum{}')]:
        t = t.replace(ch, rep)
    for a, b in UNI:
        t = t.replace(a, b)
    return t

def texify(text, size=None):
    """italics + citations -> LaTeX."""
    out, last = [], 0
    tokens = []
    # build combined token stream of italics and citations
    events = []
    for m in ITAL_RE.finditer(text):
        events.append((m.start(), m.end(), 'i', m.group(1)))
    for m in CITE_RE.finditer(text):
        events.append((m.start(), m.end(), 'c', m.group(1)))
    events.sort()
    pos = 0
    for st, en, kind, val in events:
        if st < pos:
            continue
        if st > pos:
            out.append(esc(text[pos:st]))
        if kind == 'i':
            out.append('\\textit{' + texify(val) + '}')
        else:
            out.append('\\cite{r%d}' % num[val])
        pos = en
    out.append(esc(text[pos:]))
    return ''.join(out)

def caption_text(c):
    """Strip manual 'Fig. N' / 'Table N' prefixes (LaTeX adds its own)."""
    return texify(re.sub(r'^(Fig\.|Table)\s+\d+\s+', '', c))

def ref_text_latex(doi):
    r = BY_DOI[doi]
    auth = (r['authors'] or 'Anonymous').replace(';', ',').replace(', et al.', ' et al.')
    t = r['title_cr'].replace('&amp;', '&').rstrip('.')
    jr = (r['journal'] or '').replace('&amp;', '&')
    vol = r.get('volume', '')
    pg = r.get('page') or (f"Art. no. {r['article_number']}" if r.get('article_number') else '')
    yr = r['year']
    s = f"{esc(auth)}, ``{esc(t)},'' {esc(jr)}"
    if vol: s += f", vol. {esc(str(vol))}"
    if pg: s += f", {esc(str(pg))}"
    s += f", {yr}. doi: {doi}."
    return s

# ---------- table -> LaTeX ----------
def table_latex(key):
    spec = TABLES[key]
    rows = spec['rows']
    if rows == 'AUTO_AREA_YEAR':
        stats = json.load(open(f'{ROOT}/corpus/stats.json'))
        ay = stats['area_by_year']
        rev = {}
        for r in CORPUS:
            if r['method'] == 'Review / perspective':
                rev[r['area']] = rev.get(r['area'], 0) + 1
        years = ['2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026']
        rows = []
        for a, m in sorted(ay.items()):
            tot = sum(m.values()); rv = rev.get(a, 0)
            rows.append([a] + [str(m.get(y, 0)) for y in years] + [str(tot), str(rv), str(tot - rv)])
        total = ['Total'] + [str(sum(int(r[i + 1]) for r in rows)) for i in range(len(years))]
        total += [str(len(CORPUS)), str(sum(rev.values())), str(len(CORPUS) - sum(rev.values()))]
        rows.append(total)
    header = spec['header']
    ncol = len(header)
    # column weights from content length
    weights = []
    for j in range(ncol):
        w = max([len(str(header[j]))] + [len(str(r[j])) for r in rows if len(r) > j])
        weights.append(min(max(w, 3), 80))
    tot_w = sum(weights)
    # width budget: 7.0 in total for table*, minus ~0.15in per col padding
    usable = 7.0 - 0.12 * ncol
    widths = [max(usable * w / tot_w, 0.38) for w in weights]
    scale = usable / sum(widths)
    widths = [w * scale for w in widths]

    L = []
    L.append('\\begin{table*}[!t]')
    L.append('\\caption{' + caption_text(spec['caption']) + '}')
    L.append('\\label{tab:' + key + '}')
    L.append('\\centering')
    L.append('\\footnotesize')
    L.append('\\begin{tabular}{' + ''.join('|p{%.2fin}' % w for w in widths) + '|}')
    L.append('\\hline')
    L.append(' & '.join('\\textbf{' + texify(str(h)) + '}' for h in header) + ' \\\\')
    L.append('\\hline')
    for row in rows:
        cells = []
        for j, cell in enumerate(row):
            cells.append(texify(str(cell)))
        L.append(' & '.join(cells) + ' \\\\')
        if row[0] == 'Total':
            L.append('\\hline')
    L.append('\\hline')
    L.append('\\end{tabular}')
    L.append('\\end{table*}')
    return '\n'.join(L)

FIG_W = {  # LaTeX graphic widths (inches), from design size
    'fig1_function_method_map.png': 6.9, 'fig2_prisma.png': 5.9,
    'fig2_year_trend.png': 3.35, 'fig3_method_evolution.png': 5.0,
    'fig4_area_distribution.png': 5.5, 'fig5_data_validation.png': 6.8,
    'fig7_dataset_saturation.png': 5.1, 'fig6_timeline.png': 6.4,
}
SINGLE_COL = {'fig2_year_trend.png'}

def fig_latex(path, caption):
    fname = os.path.basename(path)
    import shutil
    shutil.copy(f'{ROOT}/{path}', f'{FIGDIR}/{fname}')
    cap = caption_text(caption)
    w = FIG_W.get(fname, 4.9)
    if fname in SINGLE_COL:
        return ('\\begin{figure}[!t]\n\\caption{' + cap + '}\n\\centering\n'
                '\\includegraphics[width=\\columnwidth]{figs/' + fname + '}\n'
                '\\label{fig:' + fname + '}\n\\end{figure}')
    return (f'\\begin{{figure*}}[!t]\n\\caption{{{cap}}}\n\\centering\n'
            f'\\includegraphics[width={w}in]{{figs/{fname}}}\n'
            f'\\label{{fig:{fname}}}\n\\end{{figure*}}')

# ---------- assemble body ----------
body = []
for kind, *rest in BLOCKS:
    if kind == 'h1':
        title = re.sub(r'^\d+\.\s+', '', rest[0])
        body.append('\\section{' + texify(title) + '}')
    elif kind == 'h2':
        title = re.sub(r'^\d+\.\d+\s+', '', rest[0])
        body.append('\\subsection{' + texify(title) + '}')
    elif kind == 'p':
        body.append(texify(rest[0]))
    elif kind == 'fig':
        body.append(fig_latex(rest[0], rest[1]))
    elif kind == 'tbl':
        body.append(table_latex(rest[0]))
    elif kind == 'decl':
        body.append('\\section*{Data and Code Availability}')
        body.append('The classified and Crossref-verified corpus of 103 studies is released as a machine-readable '
                    'supplementary dataset (papers.csv), including per-paper citation counts and the screening statistics. '
                    'The complete search, screening, verification, and figure-generation scripts are publicly available at '
                    '\\url{' + 'https://github.com/touhidsiddiqueeraj-bit/-structured-scoping-review-and-classification-of-103-peer-reviewed-studies-about-AI-in-BMS' + '}, '
                    'so that every figure and count in Section III can be regenerated from the released dataset.')
        body.append('\\section*{Acknowledgment}')
        body.append('The authors would like to acknowledge the use of writing-support and language-enhancement tools, '
                    'including OpenAI ChatGPT, Grammarly, and QuillBot, during the preparation of this manuscript. '
                    'These tools were used to assist with grammar correction, readability improvement, language refinement, '
                    'and sentence restructuring. All technical content, analysis, interpretations, and research contributions '
                    'are from the authors themselves. This work received no specific funding.')

# ---------- bibliography ----------
bib = ['\\begin{thebibliography}{120}']
for i, doi in enumerate(order, 1):
    bib.append('\\bibitem{r%d}' % i)
    bib.append(ref_text_latex(doi))
bib.append('\\end{thebibliography}')

# ---------- preamble + front matter ----------
names = ', '.join(esc(n) for n, _ in AUTHORS[:-1])
authors_tex = (names + ', and ' + esc(AUTHORS[-1][0])).replace(' ', '~')

bib_lines = ['\\begin{thebibliography}{120}']
for i, doi in enumerate(order, 1):
    bib_lines.append('\\bibitem{r%d}' % i)
    bib_lines.append(ref_text_latex(doi))
bib_lines.append('\\end{thebibliography}')

REPO_URL = ('https://github.com/touhidsiddiqueeraj-bit/'
            '-structured-scoping-review-and-classification-of-103-peer-reviewed-studies-about-AI-in-BMS')

tex = r'''\documentclass[journal]{IEEEtran}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{array}
\usepackage{url}
\usepackage{cite}
\usepackage{amsmath,amssymb}
\usepackage{balance}
\begin{document}

\title{''' + esc(TITLE).replace('--', '--') + r'''}

\author{''' + authors_tex + r'''%
\thanks{Manuscript received September 2026. (Corresponding author: Hussain Touhid Siddiquee.)}%
\thanks{The authors are with Leading University, Sylhet, Bangladesh. The classified corpus,
the conference sensitivity set, and the complete analysis pipeline are publicly available at
\texttt{github.com/touhidsiddiqueeraj-bit}.}}

\markboth{IEEE Transactions Submission, September 2026}{Siddiquee et al.: Machine Learning in Battery Management Systems}

\maketitle

\begin{abstract}
''' + texify(' '.join(ABSTRACT)) + r'''
\end{abstract}

\begin{IEEEkeywords}
''' + esc(KEYWORDS.replace(';', ',')) + r'''
\end{IEEEkeywords}

''' + '\n\n'.join(body) + '\n\n' + '\n'.join(bib_lines) + r'''

\balance
\end{document}
'''

open(OUT_TEX, 'w').write(tex)
print('wrote', OUT_TEX, '| refs:', len(order))
