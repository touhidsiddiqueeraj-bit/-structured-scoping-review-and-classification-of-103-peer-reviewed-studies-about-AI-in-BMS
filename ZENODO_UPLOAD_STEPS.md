# Zenodo upload — step by step

Package ready: `zenodo_upload.zip` (or the loose directory `zenodo_upload/`).

> **Record correction (October 2026):** the already-published Zenodo record
> 10.5281/zenodo.23436202 is registered with resource type *Preprint*.
> The deposit is a dataset + code release; `zenodo_metadata.json` now carries
> `upload_type: dataset`. Please apply the same one-click correction on the
> live record: Zenodo -> the record -> Edit -> Change resource type -> Dataset
> -> Save (a new version of the record is created; the DOI is preserved).
Everything inside runs standalone — verified: the full regeneration pipeline
(eligible corpus → stats → provenance logs → consistency checks → reliability
selftest) was executed from the extracted zip in a clean directory.

## 1. Reserve the DOI (account needed; nihma/RDM staff can do this)

Option A (web):
1. Log in at zenodo.org → **+ New upload**.
2. Fill the form — fastest way: paste `zenodo_upload/zenodo_metadata.json`
   (it is in Zenodo's own API schema: title, creators, description, license
   cc-by-4.0, keywords, related identifier to the GitHub repo).
   If the form import isn't offered, copy the fields manually from the JSON.
3. **Before publishing**: click *Reserve DOI* on the right panel → Zenodo
   shows a reserved DOI like `10.5281/zenodo.14xxxxxx`.
4. Drag `zenodo_upload.zip` (or the files) as the upload content. Wait for
   the preview/validation pass.
5. **Publish**. DOI goes live immediately and cannot be deleted; files can
   be versioned later.

Option B (API, if a token is available):
```bash
TOKEN=xxxx  # from zenodo.org/account/settings/applications
curl -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
     -d @zenodo_upload/zenodo_metadata.json \
     https://zenodo.org/api/deposits            # create draft
# → PATCH the deposit links.deposit_uploads ... (files upload needs multipart)
# reserve DOI: the draft response already contains a reserved concept DOI
```

## 2. Inject the DOI into the manuscript — DONE

Done 2026-10-17: `ZENODO_DOI = '10.5281/zenodo.23436202'` in `corpus/build_tex.py`;
both citation sites update automatically on rebuild (author-block thanks line
and the *Data and Code Availability* section). The previously-GitHub-only
artifact note is replaced: the deposit is the deposit of record, GitHub is a
development mirror.

Optionally update the citation line in `zenodo_upload/README.md`
(`zenodo.23436202` → real DOI) and re-zip via `python3 corpus/make_zenodo_package.py`
before uploading — a README that self-cites the real DOI looks best,
but publishing once with the placeholder in README and versioning later is also fine.

## 3. Bio/RDM checklist

- [ ] License set to **CC-BY-4.0** (both web field and README/LICENSE).
- [ ] **Related identifier**: GitHub repo, relation `isSupplementedBy`.
- [ ] All 45 files present, incl. `zenodo_metadata.json` + README + LICENSE
      (now incl. `tagging_terms.json`, `sensitivity_label_noise.{py,json}`,
      `per_year_denominators.json`, `pool.py`, `crossref_year_counts.py`,
      and the expanded `screening_log.csv` — 1,550 pool decisions + 5
      forced-seed entries).
- [ ] deposit published → copy DOI → set `ZENODO_DOI` → rebuild PDF → attach to
      ScholarOne/Editorial Manager as the data link.
