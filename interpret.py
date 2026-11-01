"""Rule-based interpretation. Every sentence comes from a fixed rule, and every
citation comes from references/references.json, so nothing can be invented."""

def nz(x, d=3):
    s = f"{x:.{d}f}"
    if s.startswith("0."):
        return s[1:]
    if s.startswith("-0."):
        return "-" + s[2:]
    return s


def ptxt(p):
    return "p < .001" if p < 0.001 else f"p = {nz(p)}"


def cap(t):
    return t[:1].upper() + t[1:] if t else t


class Cites:
    """Collects the citation keys used so the reference list matches the text."""
    def __init__(self, refs):
        self.refs, self.used = refs, []

    def __call__(self, *keys):
        for k in keys:
            if k not in self.used:
                self.used.append(k)
        return "(" + "; ".join(self.refs[k]["cite"] for k in keys) + ")"

    def reference_list(self):
        return sorted((self.refs[k]["apa"] for k in self.used), key=lambda s: s.lower())


def lab(labels, name):
    return labels.get(name, name)


def method_text(res, c):
    s = []
    ver = f" {res['version']}" if res.get("version") else ""
    est = res.get("estimator") or "the default estimator"
    s.append(f"Analyses were conducted in Mplus{ver} {c('muthen2017')} using {est} estimation"
             + (f" with robust standard errors {c('yuan2000')}" if est == "MLR" else "") + ".")
    if res.get("n"):
        s.append(f"The analysis included N = {res['n']:,} observations.")
    if res.get("patterns") and res["patterns"] > 1 and est in ("MLR", "ML", "MLF", "MLM", "MLMV"):
        s.append(f"Missing data were handled with full information maximum likelihood (FIML) {c('enders2010')}; "
                 f"Mplus identified {res['patterns']} missing-data patterns.")
    return " ".join(s)


def rate_cfi(v):
    return "good" if v >= .95 else "acceptable" if v >= .90 else "poor"


def rate_rmsea(v):
    return "good" if v <= .06 else "acceptable" if v <= .08 else "poor"


def rate_srmr(v):
    return "good" if v <= .08 else "poor"


def fit_text(res, c):
    f = res["fit"]
    if "cfi" not in f:
        return "Model fit statistics were not found in this output."
    est = res.get("estimator")
    chi = f"χ²({f['df']}) = {f['chi2']:,.2f}, {ptxt(f['chi2_p'])}"
    out = [f"The model showed the following fit: {chi}, CFI = {nz(f['cfi'])}, TLI = {nz(f['tli'])}, "
           f"RMSEA = {nz(f['rmsea'])} (90% CI [{nz(f['rmsea_lo'])}, {nz(f['rmsea_hi'])}]), SRMR = {nz(f['srmr'])}."]
    if est in ("MLR", "MLM", "MLMV", "WLSMV") and f.get("scaling"):
        out.append("The chi-square value is a scaled (robust) statistic.")
    ratings = {"CFI": rate_cfi(f["cfi"]), "TLI": rate_cfi(f["tli"]),
               "RMSEA": rate_rmsea(f["rmsea"]), "SRMR": rate_srmr(f["srmr"])}
    cfi_tli = (f"CFI and TLI were both {ratings['CFI']}" if ratings['CFI'] == ratings['TLI']
               else f"CFI was {ratings['CFI']} and TLI was {ratings['TLI']}")
    out.append(f"{cfi_tli} (≥ .95 indicates good fit, ≥ .90 acceptable) {c('hu1999', 'kline2016')}. "
               f"RMSEA was {ratings['RMSEA']} (≤ .06 good, ≤ .08 acceptable) {c('hu1999', 'browne1993')}, "
               f"and SRMR was {ratings['SRMR']} (≤ .08) {c('hu1999')}.")
    if f["chi2_p"] < .05 and (res.get("n") or 0) >= 300:
        out.append(f"The chi-square test was significant, which is common in large samples and is usually interpreted alongside approximate fit indices {c('kline2016')}.")
    good = sum(v == "good" for v in ratings.values())
    ok = sum(v in ("good", "acceptable") for v in ratings.values())
    if good == 4:
        out.append("Overall, the model fit the data well.")
    elif ok == 4:
        out.append("Overall, the model showed acceptable fit.")
    else:
        poor = [k for k, v in ratings.items() if v == "poor"]
        out.append(f"Overall, fit was not fully satisfactory ({', '.join(poor)} outside the usual cut-offs); model modification or a different specification should be considered with theoretical justification.")
    return " ".join(out)


def loadings(res, labels, c):
    """Standardized loadings per factor."""
    rows = [r for r in res["stdyx"] if r["block"].endswith(" BY")]
    fac = {}
    for r in rows:
        fac.setdefault(r["block"].split()[0], []).append(r)
    text = []
    weak_all = []
    for f, items in fac.items():
        vals = [i["est"] for i in items]
        s = (f"For {lab(labels, f)}, standardized loadings ranged from {nz(min(vals))} to {nz(max(vals))}")
        weak = [i["name"] for i in items if i["est"] < .50]
        if weak:
            s += f"; {', '.join(weak)} fell below .50"
            weak_all += weak
        s += "."
        text.append(s)
    if text:
        text.append(f"Loadings of .50 or higher are generally considered adequate and .70 or higher strong {c('hair2019')}.")
    return fac, " ".join(text)


def factor_corr(res, labels, c):
    lat = set(res["latent"])
    rows = [r for r in res["stdyx"] if r["block"].endswith(" WITH") and r["block"].split()[0] in lat and r["name"] in lat]
    if not rows:
        return rows, ""
    parts = []
    for r in rows:
        a = abs(r["est"])
        size = "large" if a >= .50 else "moderate" if a >= .30 else "small" if a >= .10 else "negligible"
        a_n, b_n = lab(labels, r["block"].split()[0]), lab(labels, r["name"])
        parts.append(f"{a_n} and {b_n} were {'positively' if r['est'] > 0 else 'negatively'} correlated (r = {nz(r['est'])}, {ptxt(r['p'])}; {size})")
    return rows, "; ".join(parts).capitalize() + f". Correlation sizes follow common benchmarks of .10, .30 and .50 {c('cohen1988')}."


def reliability(res, labels, c):
    rows = [r for r in res["unstd"] if r["block"].startswith("New/Additional") and r["name"].upper().startswith("OMEGA")]
    if not rows:
        return rows, ""
    parts = []
    for r in rows:
        v = r["est"]
        word = "strong" if v >= .80 else "acceptable" if v >= .70 else "below the usual .70 benchmark"
        parts.append(f"{lab(labels, r['name'])} (ω = {nz(v)}, {word})")
    return rows, ("McDonald's omega indicated reliability for " + "; ".join(parts) +
                  f". Values of .70 or higher are usually considered acceptable {c('nunnally1994')}, and omega is preferred over Cronbach's alpha when loadings differ {c('mcdonald1999', 'hayes2020')}.")


def structural(res, labels, c):
    lat = set(res["latent"])
    unstd = {(r["block"], r["name"]): r for r in res["unstd"]}
    rows = [r for r in res["stdyx"] if r["block"].endswith(" ON")]
    if not rows:
        return rows, ""
    sents = []
    for r in rows:
        dv = r["block"].split()[0]
        u = unstd.get((r["block"], r["name"]), r)
        sig = u["p"] < .05
        verb = "was not significantly related to" if not sig else ("positively predicted" if r["est"] > 0 else "negatively predicted")
        if not sig:
            sents.append(cap(f"{lab(labels, r['name'])} {verb} {lab(labels, dv)} (β = {nz(r['est'])}, {ptxt(u['p'])})."))
        else:
            sents.append(cap(f"{lab(labels, r['name'])} {verb} {lab(labels, dv)} (β = {nz(r['est'])}, {ptxt(u['p'])})."))
    note = ""
    if (res.get("n") or 0) > 10000:
        note = f" With a very large sample, even small effects are statistically significant, so the size of the coefficients should guide interpretation {c('kline2016')}."
    r2 = res["rsquare"]["latent"]
    if r2:
        note += " Variance explained: " + "; ".join(f"{lab(labels, x['name'])} R² = {nz(x['est'])}" for x in r2) + "."
    return rows, " ".join(sents) + note


def effects_text(res, labels, c):
    effs = res.get("effects_std") or res.get("effects")
    out = []
    for e in effs or []:
        ind = e["total_indirect"] or e["indirect"]
        if not ind:
            continue
        x, y = lab(labels, e["from"]), lab(labels, e["to"])
        sig_i = ind[3] < .05
        s = (f"The standardized indirect effect of {x} on {y} was β = {nz(ind[0])} (SE = {nz(ind[1])}, {ptxt(ind[3])})")
        if e["direct"]:
            d = e["direct"]
            s += f", the direct effect was β = {nz(d[0])} ({ptxt(d[3])})"
        if e["total"]:
            t = e["total"]
            s += f", and the total effect was β = {nz(t[0])} ({ptxt(t[3])})"
        s += "."
        if e["direct"] and sig_i:
            same = (ind[0] > 0) == (e["direct"][0] > 0)
            if e["direct"][3] < .05:
                kind = "complementary mediation (indirect and direct effects share a sign)" if same else "competitive mediation (indirect and direct effects have opposite signs)"
            else:
                kind = "indirect-only mediation"
            s += f" This pattern is consistent with {kind} {c('zhao2010')}."
        elif not sig_i:
            s += " The indirect effect was not statistically significant."
        s += f" Indirect effects here were tested with the delta method; bootstrapped confidence intervals are generally recommended where available {c('hayes2018')}."
        out.append(s)
    return " ".join(out)
