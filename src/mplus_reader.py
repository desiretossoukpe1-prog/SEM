"""Read an Mplus output (.out) file and return the results as plain Python data.

Only the text layout of the Mplus output is used, so no Mplus installation is needed.
"""
import re

NUM = r"-?\d+\.\d+"
ROW = re.compile(rf"^\s+(\S+)\s+({NUM})\s+({NUM})\s+({NUM})\s+({NUM})\s*$")
HEAD = re.compile(r"^\s*(\S+)\s+(BY|ON|WITH)\s*$")
PLAIN_HEADS = ("Intercepts", "Means", "Variances", "Residual Variances",
               "Thresholds", "New/Additional Parameters", "Scales")


def _floats(m):
    return tuple(float(x) for x in m.groups()[-4:])


def _find(lines, test, start=0):
    for i in range(start, len(lines)):
        if test(lines[i].strip()):
            return i
    return None


def _slice(lines, start_test, stop_tests, start=0):
    a = _find(lines, start_test, start)
    if a is None:
        return [], None
    b = len(lines)
    for i in range(a + 1, len(lines)):
        s = lines[i].strip()
        if any(t(s) for t in stop_tests):
            b = i
            break
    return lines[a:b], a


def parse_rows(block):
    """Parse a block of parameter rows into a list of dicts."""
    rows, label = [], None
    for ln in block:
        h = HEAD.match(ln)
        if h:
            label = f"{h.group(1)} {h.group(2)}"
            continue
        s = ln.strip()
        if s in PLAIN_HEADS:
            label = s
            continue
        m = ROW.match(ln)
        if m and label:
            est, se, z, p = _floats(m)
            rows.append({"block": label, "name": m.group(1),
                         "est": est, "se": se, "z": z, "p": p})
    return rows


def parse_effects(block):
    out, cur, state, path = [], None, None, []
    for ln in block:
        s = ln.strip()
        m = re.match(r"Effects from (\S+) to (\S+)", s)
        if m:
            cur = {"from": m.group(1), "to": m.group(2), "total": None,
                   "total_indirect": None, "indirect": None,
                   "direct": None, "specific": []}
            out.append(cur)
            state = None
            continue
        if cur is None:
            continue
        m = re.match(rf"^(Total indirect|Total|Indirect)\s+({NUM})\s+({NUM})\s+({NUM})\s+({NUM})$", s)
        if m:
            key = {"Total indirect": "total_indirect", "Total": "total",
                   "Indirect": "indirect"}[m.group(1)]
            cur[key] = _floats(m)
            state = None
            continue
        if re.match(r"Specific indirect \d+", s):
            state, path = "spec", []
            continue
        if s == "Direct":
            state, path = "direct", []
            continue
        if state in ("spec", "direct"):
            m = re.match(rf"^(\S+)\s+({NUM})\s+({NUM})\s+({NUM})\s+({NUM})$", s)
            if m:
                path.append(m.group(1))
                vals = _floats(m)
                if state == "spec":
                    cur["specific"].append({"path": list(path), "vals": vals})
                else:
                    cur["direct"] = vals
                state = None
            elif re.match(r"^\S+$", s):
                path.append(s)
    return out


def parse_rsquare(block):
    obs, lat, mode = [], [], None
    for ln in block:
        s = ln.strip()
        if s.startswith("Observed"):
            mode = "obs"
        elif s.startswith("Latent"):
            mode = "lat"
        m = ROW.match(ln)
        if m and mode:
            est, se, z, p = _floats(m)
            (obs if mode == "obs" else lat).append({"name": m.group(1), "est": est, "se": se, "z": z, "p": p})
    return {"observed": obs, "latent": lat}


def _first(pattern, text, flags=0, cast=float):
    m = re.search(pattern, text, flags)
    if not m:
        return None
    vals = [cast(g) for g in m.groups()]
    return vals[0] if len(vals) == 1 else tuple(vals)


def read_output(path):
    text = open(path, encoding="utf-8", errors="replace").read()
    lines = text.splitlines()
    res = {"file": path}

    res["version"] = _first(r"Mplus VERSION\s+(\S+)", text, cast=str)
    m = re.search(r"^\s*TITLE:\s*(.*)$", text, re.M)
    res["title"] = m.group(1).strip() if m else None
    res["n"] = _first(r"Number of observations\s+(\d+)", text, cast=int)
    res["estimator"] = _first(r"^Estimator\s+(\S+)", text, re.M, cast=str)
    res["patterns"] = _first(r"Number of missing data patterns\s+(\d+)", text, cast=int)
    res["terminated_normally"] = "THE MODEL ESTIMATION TERMINATED NORMALLY" in text

    fit = {}
    fit["params"] = _first(r"Number of Free Parameters\s+(\d+)", text, cast=int)
    chi = re.search(r"Chi-Square Test of Model Fit\s+Value\s+([\d.]+)\*?\s+Degrees of Freedom\s+(\d+)\s+P-Value\s+([\d.]+)", text)
    if chi:
        fit["chi2"], fit["df"], fit["chi2_p"] = float(chi.group(1)), int(chi.group(2)), float(chi.group(3))
    fit["scaling"] = _first(r"Chi-Square Test of Model Fit.*?Scaling Correction Factor\s+([\d.]+)", text, re.S)
    r = re.search(r"RMSEA.*?Estimate\s+([\d.]+)\s+90 Percent C\.I\.\s+([\d.]+)\s+([\d.]+)", text, re.S)
    if r:
        fit["rmsea"], fit["rmsea_lo"], fit["rmsea_hi"] = (float(x) for x in r.groups())
    c = re.search(r"CFI\s+([\d.]+)\s+TLI\s+([\d.]+)", text)
    if c:
        fit["cfi"], fit["tli"] = float(c.group(1)), float(c.group(2))
    fit["srmr"] = _first(r"SRMR.*?Value\s+([\d.]+)", text, re.S)
    fit["aic"] = _first(r"Akaike \(AIC\)\s+([\d.]+)", text)
    fit["bic"] = _first(r"Bayesian \(BIC\)\s+([\d.]+)", text)
    res["fit"] = fit

    warnings = []
    for i, ln in enumerate(lines):
        if ln.strip().startswith("*** WARNING") or ln.strip().startswith("*** ERROR"):
            chunk = []
            for nxt in lines[i + 1:]:
                if not nxt.strip() or nxt.strip().startswith("***"):
                    break
                chunk.append(nxt.strip())
            warnings.append(" ".join(chunk))
    if "MAY NOT BE" in text and "TRUSTWORTHY" in text:
        warnings.append("Mplus reported that standard errors may not be trustworthy for some parameters (possible non-identification).")
    if "DID NOT TERMINATE NORMALLY" in text:
        warnings.append("The model estimation did not terminate normally.")
    res["warnings"] = warnings

    stops_main = [lambda s: s == "QUALITY OF NUMERICAL RESULTS",
                  lambda s: s == "STANDARDIZED MODEL RESULTS"]
    blk, _ = _slice(lines, lambda s: s == "MODEL RESULTS", stops_main)
    res["unstd"] = parse_rows(blk)

    st, a = _slice(lines, lambda s: s == "STDYX Standardization",
                   [lambda s: s == "R-SQUARE", lambda s: s.startswith("STDY Standardization"),
                    lambda s: s.startswith("STD Standardization"),
                    lambda s: s.startswith("TOTAL, TOTAL INDIRECT"),
                    lambda s: s.startswith("TECHNICAL")],
                   start=_find(lines, lambda s: s == "STANDARDIZED MODEL RESULTS") or 0)
    res["stdyx"] = parse_rows(st)

    rs, _ = _slice(lines, lambda s: s == "R-SQUARE",
                   [lambda s: s.startswith("TOTAL, TOTAL INDIRECT"),
                    lambda s: s.startswith("TECHNICAL"), lambda s: s.startswith("Beginning Time")])
    res["rsquare"] = parse_rsquare(rs)

    eff, _ = _slice(lines, lambda s: s.startswith("TOTAL, TOTAL INDIRECT"),
                    [lambda s: s.startswith("STANDARDIZED TOTAL"), lambda s: s.startswith("TECHNICAL")])
    res["effects"] = parse_effects(eff)
    seff, _ = _slice(lines, lambda s: s.startswith("STANDARDIZED TOTAL, TOTAL INDIRECT"),
                     [lambda s: s.startswith("TECHNICAL"), lambda s: s.startswith("Beginning Time"),
                      lambda s: s.startswith("MUTHEN")])
    res["effects_std"] = parse_effects(seff)

    res["latent"] = sorted({r["block"].split()[0] for r in res["unstd"] + res["stdyx"] if r["block"].endswith(" BY")})
    return res


if __name__ == "__main__":
    import json, sys
    print(json.dumps(read_output(sys.argv[1]), indent=1)[:4000])
