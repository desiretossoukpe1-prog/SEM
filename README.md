# SEM report automation for Mplus

Turns a Mplus output file (`.out`) into a Word and Markdown results report with APA-style tables,
rule-based interpretations, and a reference list. Citations come only from `references/references.json`,
so the program cannot invent a source.

## What it reads and writes
- **Reads:** Mplus `.out` files. Ask Mplus for `OUTPUT: STDYX;` so standardized results are included
  (add `TECH1`, `PATTERNS` or other options freely).
- **Writes:** `reports/<name>_report.docx` and `reports/<name>_report.md`.
- **Sections:** analysis details, model fit, factor loadings, factor correlations, McDonald's omega
  (parameters named `OMEGA...`), structural paths, direct/indirect/total effects, Mplus warnings, references.

## Folder structure
```
data/outputs/        put your .out files here
reports/             generated reports
src/mplus_reader.py  reads the Mplus text output
src/interpret.py     interpretation rules and cut-offs
src/build_report.py  builds the Word and Markdown reports
config/labels.json   readable names for your variables (edit this)
references/references.json  the only sources the report may cite (add yours)
examples/            two condensed example outputs
tests/               checks that the reader finds the right numbers
docs/notebooklm_prompt.md   optional manual step for AI-written discussion
.github/workflows/report.yml  runs everything automatically on GitHub
```

## Use it on your computer
```
pip install -r requirements.txt
python src/build_report.py data/outputs/my_model.out
python src/build_report.py --all
python -m unittest discover -s tests
```

## Use it on GitHub
1. Create a new repository on github.com and upload all of these files (or push them with git).
2. Add a Mplus output to `data/outputs/` and commit it.
3. Open the **Actions** tab. The workflow "Build SEM reports" runs, and the reports appear in
   the `reports/` folder and as a downloadable artifact.

Only commit Mplus output files. Do not commit raw data; `.gitignore` blocks `.csv`, `.dat` and `.sav`.
If your repository is public, anyone can read the outputs you commit.

## Customize
- **Names:** edit `config/labels.json` (for example `"T3DISC": "perceived disciplinary climate"`).
  Check that each label matches what the variable really measures.
- **Sources:** add entries to `references/references.json`, then use them in `src/interpret.py`
  with `c("key")`.
- **Cut-offs:** change them in `src/interpret.py` (fit: CFI/TLI .95 and .90, RMSEA .06 and .08, SRMR .08).

## What it does and does not do
- Works for CFA and SEM outputs with ML-family estimators (ML, MLR, MLM) and STDYX results.
- Not yet tested on multi-group models, WLSMV or categorical thresholds, bootstrapped confidence
  intervals, or multilevel models. Upload an example of each and the reader can be extended.
- The text is a draft. Verify every statement and every reference before using it
  (check the page, edition and DOI of each source).
- Reliability thresholds and the mediation labels are simple rules, not a substitute for judgment.
