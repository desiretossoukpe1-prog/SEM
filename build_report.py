"""Build a Word (.docx) and Markdown results report from Mplus output files.

Usage:
    python src/build_report.py path/to/model.out
    python src/build_report.py --all          # every .out file in data/outputs
"""
import argparse, glob, json, os, re, sys

sys.path.insert(0, os.path.dirname(__file__))
from mplus_reader import read_output
import interpret as I
lab = I.lab

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def pcell(row):
    """p-value for a table cell; Mplus prints 999 for fixed (reference) parameters."""
    if row["z"] >= 999 or row["p"] >= 999:
        return "— (fixed)"
    return "< .001" if row["p"] < .001 else I.nz(row["p"])


def build_sections(res, labels, refs):
    c = I.Cites(refs)
    S = []  # list of (kind, payload)
    S.append(("h1", res.get("title") or os.path.basename(res["file"])))
    if not res["terminated_normally"]:
        S.append(("p", "**Warning: Mplus did not report normal termination. Do not interpret these results until this is resolved.**"))
    S.append(("h2", "Analysis"))
    S.append(("p", I.method_text(res, c)))

    S.append(("h2", "Model fit"))
    S.append(("p", I.fit_text(res, c)))
    f = res["fit"]
    if "cfi" in f:
        S.append(("table", {"title": "Table 1. Model fit indices",
                            "header": ["Index", "Value"],
                            "rows": [["χ² (df)", f"{f['chi2']:,.2f} ({f['df']})"], ["p", "< .001" if f["chi2_p"] < .001 else I.nz(f["chi2_p"])],
                                     ["CFI", I.nz(f["cfi"])], ["TLI", I.nz(f["tli"])],
                                     ["RMSEA [90% CI]", f"{I.nz(f['rmsea'])} [{I.nz(f['rmsea_lo'])}, {I.nz(f['rmsea_hi'])}]"],
                                     ["SRMR", I.nz(f["srmr"])]]}))

    fac, ltxt = I.loadings(res, labels, c)
    if fac:
        S.append(("h2", "Measurement model"))
        S.append(("p", ltxt))
        unstd = {(r["block"], r["name"]): r for r in res["unstd"]}
        rows = []
        for fname, items in fac.items():
            for it in items:
                u = unstd.get((it["block"], it["name"]), it)
                rows.append([lab(labels, fname).capitalize(), it["name"], I.nz(it["est"]), I.nz(it["se"]),
                             pcell(u)])
        S.append(("table", {"title": "Table 2. Standardized factor loadings",
                            "header": ["Factor", "Item", "β", "SE", "p"], "rows": rows}))

    cr, ctxt = I.factor_corr(res, labels, c)
    if cr:
        S.append(("h2", "Relations among factors"))
        S.append(("p", ctxt))

    rr, rtxt = I.reliability(res, labels, c)
    if rr:
        S.append(("h2", "Reliability"))
        S.append(("p", rtxt))
        S.append(("table", {"title": "Table 3. McDonald's omega",
                            "header": ["Scale", "ω", "SE"],
                            "rows": [[lab(labels, r["name"]).capitalize(), I.nz(r["est"]), I.nz(r["se"])] for r in rr]}))

    sr, stxt = I.structural(res, labels, c)
    if sr:
        S.append(("h2", "Structural model"))
        S.append(("p", stxt))
        unstd = {(r["block"], r["name"]): r for r in res["unstd"]}
        rows = []
        for r in sr:
            u = unstd.get((r["block"], r["name"]), r)
            rows.append([f"{lab(labels, r['name'])} → {lab(labels, r['block'].split()[0])}", I.nz(u["est"]), I.nz(r["est"]), I.nz(r["se"]),
                         pcell(u)])
        S.append(("table", {"title": "Table 4. Structural paths",
                            "header": ["Path", "B", "β", "SE (β)", "p"], "rows": rows}))

    etxt = I.effects_text(res, labels, c)
    if etxt:
        S.append(("h2", "Indirect effects"))
        S.append(("p", etxt))
        rows = []
        for e in res.get("effects_std") or res.get("effects"):
            def cell(v): return "—" if not v else f"{I.nz(v[0])} ({I.ptxt(v[3]).replace('p ', 'p')})"
            rows.append([f"{lab(labels, e['from'])} → {lab(labels, e['to'])}", cell(e["direct"]),
                         cell(e["total_indirect"] or e["indirect"]), cell(e["total"])])
        S.append(("table", {"title": "Table 5. Standardized direct, indirect and total effects",
                            "header": ["Effect", "Direct", "Indirect", "Total"], "rows": rows}))

    if res["warnings"]:
        S.append(("h2", "Notes from Mplus to check"))
        for w in res["warnings"]:
            S.append(("bullet", w))

    S.append(("h2", "References"))
    for r in c.reference_list():
        S.append(("ref", r))
    S.append(("note", "Draft generated automatically from the Mplus output. Check every statement and citation against the original sources before use."))
    return S


def to_markdown(S):
    out = []
    for kind, x in S:
        if kind == "h1": out.append(f"# {x}\n")
        elif kind == "h2": out.append(f"\n## {x}\n")
        elif kind == "p": out.append(x + "\n")
        elif kind == "bullet": out.append(f"- {x}")
        elif kind == "ref": out.append(x + "\n")
        elif kind == "note": out.append(f"\n*{x}*\n")
        elif kind == "table":
            out.append(f"**{x['title']}**\n")
            out.append("| " + " | ".join(x["header"]) + " |")
            out.append("|" + "---|" * len(x["header"]))
            for r in x["rows"]:
                out.append("| " + " | ".join(r) + " |")
            out.append("")
    return "\n".join(out)


def _runs(par, text):
    """Add text to a paragraph; *x* = italic, **x** = bold."""
    for tok in re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*)", text):
        if not tok: continue
        if tok.startswith("**"): par.add_run(tok[2:-2]).bold = True
        elif tok.startswith("*"): par.add_run(tok[1:-1]).italic = True
        else: par.add_run(tok)


def to_docx(S, path):
    from docx import Document
    from docx.shared import Pt, Inches
    d = Document()
    st = d.styles["Normal"]; st.font.name = "Times New Roman"; st.font.size = Pt(12)
    for s in d.sections:
        s.left_margin = s.right_margin = s.top_margin = s.bottom_margin = Inches(1)
    for kind, x in S:
        if kind == "h1": d.add_heading(x, 0)
        elif kind == "h2": d.add_heading(x, 2)
        elif kind == "p": _runs(d.add_paragraph(), x)
        elif kind == "bullet": _runs(d.add_paragraph(style="List Bullet"), x)
        elif kind == "ref":
            p = d.add_paragraph(); _runs(p, x)
            p.paragraph_format.left_indent = Inches(0.5); p.paragraph_format.first_line_indent = Inches(-0.5)
        elif kind == "note":
            p = d.add_paragraph(); r = p.add_run(x); r.italic = True; r.font.size = Pt(10)
        elif kind == "table":
            cap = d.add_paragraph(); cap.add_run(x["title"]).bold = True
            t = d.add_table(rows=1, cols=len(x["header"])); t.style = "Table Grid"
            for i, h in enumerate(x["header"]):
                t.rows[0].cells[i].text = ""; t.rows[0].cells[i].paragraphs[0].add_run(h).bold = True
            for r in x["rows"]:
                cells = t.add_row().cells
                for i, v in enumerate(r): cells[i].text = str(v)
            d.add_paragraph()
    d.save(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--out", default=os.path.join(ROOT, "reports"))
    ap.add_argument("--labels", default=os.path.join(ROOT, "config", "labels.json"))
    ap.add_argument("--refs", default=os.path.join(ROOT, "references", "references.json"))
    a = ap.parse_args()
    files = a.files or []
    if a.all: files += sorted(glob.glob(os.path.join(ROOT, "data", "outputs", "*.out")))
    if not files: sys.exit("No .out files given. Use a path or --all.")
    labels = json.load(open(a.labels, encoding="utf-8")) if os.path.exists(a.labels) else {}
    refs = json.load(open(a.refs, encoding="utf-8"))
    os.makedirs(a.out, exist_ok=True)
    for f in files:
        res = read_output(f)
        S = build_sections(res, labels, refs)
        base = os.path.join(a.out, os.path.splitext(os.path.basename(f))[0] + "_report")
        open(base + ".md", "w", encoding="utf-8").write(to_markdown(S))
        to_docx(S, base + ".docx")
        print("wrote", base + ".md and .docx")


if __name__ == "__main__":
    main()
