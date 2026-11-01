# FINAL AT LARGE PROJECT SEM MEDIATION


## Analysis

Analyses were conducted in Mplus 9.1.1 (Muthén & Muthén, 1998–2017) using MLR estimation with robust standard errors (Yuan & Bentler, 2000). The analysis included N = 255,443 observations. Missing data were handled with full information maximum likelihood (FIML) (Enders, 2010); Mplus identified 443 missing-data patterns.


## Model fit

The model showed the following fit: χ²(57) = 19,429.65, p < .001, CFI = .978, TLI = .970, RMSEA = .036 (90% CI [.036, .037]), SRMR = .033. The chi-square value is a scaled (robust) statistic. CFI and TLI were both good (≥ .95 indicates good fit, ≥ .90 acceptable) (Hu & Bentler, 1999; Kline, 2016). RMSEA was good (≤ .06 good, ≤ .08 acceptable) (Hu & Bentler, 1999; Browne & Cudeck, 1993), and SRMR was good (≤ .08) (Hu & Bentler, 1999). The chi-square test was significant, which is common in large samples and is usually interpreted alongside approximate fit indices (Kline, 2016). Overall, the model fit the data well.

**Table 1. Model fit indices**

| Index | Value |
|---|---|
| χ² (df) | 19,429.65 (57) |
| p | < .001 |
| CFI | .978 |
| TLI | .970 |
| RMSEA [90% CI] | .036 [.036, .037] |
| SRMR | .033 |


## Measurement model

For perceived disciplinary climate, standardized loadings ranged from .533 to .883. For student behavior stress, standardized loadings ranged from .481 to .942; TT3G52F, TT3G52H fell below .50. For classroom management self-efficacy, standardized loadings ranged from .644 to .818. Loadings of .50 or higher are generally considered adequate and .70 or higher strong (Hair et al., 2019).

**Table 2. Standardized factor loadings**

| Factor | Item | β | SE | p |
|---|---|---|---|---|
| Perceived disciplinary climate | TT3G41A | .783 | .001 | — (fixed) |
| Perceived disciplinary climate | TT3G41BR | .533 | .002 | < .001 |
| Perceived disciplinary climate | TT3G41C | .883 | .001 | < .001 |
| Perceived disciplinary climate | TT3G41D | .851 | .001 | < .001 |
| Student behavior stress | TT3G52F | .481 | .002 | — (fixed) |
| Student behavior stress | TT3G52G | .942 | .002 | < .001 |
| Student behavior stress | TT3G52H | .489 | .002 | < .001 |
| Classroom management self-efficacy | TT3G34D | .784 | .001 | — (fixed) |
| Classroom management self-efficacy | TT3G34F | .644 | .002 | < .001 |
| Classroom management self-efficacy | TT3G34H | .818 | .001 | < .001 |
| Classroom management self-efficacy | TT3G34I | .803 | .001 | < .001 |


## Structural model

Perceived disciplinary climate positively predicted student behavior stress (β = .519, p < .001). Student behavior stress negatively predicted classroom management self-efficacy (β = -.021, p < .001). Perceived disciplinary climate negatively predicted classroom management self-efficacy (β = -.275, p < .001). Gender negatively predicted student behavior stress (β = -.040, p < .001). Years of teaching experience was not significantly related to student behavior stress (β = .001, p = .466). Gender negatively predicted classroom management self-efficacy (β = -.032, p < .001). Years of teaching experience positively predicted classroom management self-efficacy (β = .039, p < .001). With a very large sample, even small effects are statistically significant, so the size of the coefficients should guide interpretation (Kline, 2016). Variance explained: student behavior stress R² = .269; classroom management self-efficacy R² = .088.

**Table 4. Structural paths**

| Path | B | β | SE (β) | p |
|---|---|---|---|---|
| perceived disciplinary climate → student behavior stress | .376 | .519 | .002 | < .001 |
| student behavior stress → classroom management self-efficacy | -.025 | -.021 | .003 | < .001 |
| perceived disciplinary climate → classroom management self-efficacy | -.236 | -.275 | .003 | < .001 |
| gender → student behavior stress | -.040 | -.040 | .002 | < .001 |
| years of teaching experience → student behavior stress | .001 | .001 | .002 | .466 |
| gender → classroom management self-efficacy | -.038 | -.032 | .002 | < .001 |
| years of teaching experience → classroom management self-efficacy | .021 | .039 | .002 | < .001 |


## Indirect effects

The standardized indirect effect of perceived disciplinary climate on classroom management self-efficacy was β = -.011 (SE = .001, p < .001), the direct effect was β = -.275 (p < .001), and the total effect was β = -.286 (p < .001). This pattern is consistent with complementary mediation (indirect and direct effects share a sign) (Zhao et al., 2010). Indirect effects here were tested with the delta method; bootstrapped confidence intervals are generally recommended where available (Hayes, 2018).

**Table 5. Standardized direct, indirect and total effects**

| Effect | Direct | Indirect | Total |
|---|---|---|---|
| perceived disciplinary climate → classroom management self-efficacy | -.275 (p< .001) | -.011 (p< .001) | -.286 (p< .001) |


## Notes from Mplus to check

- Data set contains cases with missing on all variables except x-variables.  These cases were not included in the analysis. Number of cases with missing on all variables except x-variables:  5983 1 WARNING(S) FOUND IN THE INPUT INSTRUCTIONS

## References

Browne, M. W., & Cudeck, R. (1993). Alternative ways of assessing model fit. In K. A. Bollen & J. S. Long (Eds.), *Testing structural equation models* (pp. 136–162). Sage.

Enders, C. K. (2010). *Applied missing data analysis*. Guilford Press.

Hair, J. F., Black, W. C., Babin, B. J., & Anderson, R. E. (2019). *Multivariate data analysis* (8th ed.). Cengage.

Hayes, A. F. (2018). *Introduction to mediation, moderation, and conditional process analysis: A regression-based approach* (2nd ed.). Guilford Press.

Hu, L., & Bentler, P. M. (1999). Cutoff criteria for fit indexes in covariance structure analysis: Conventional criteria versus new alternatives. *Structural Equation Modeling, 6*(1), 1–55. https://doi.org/10.1080/10705519909540118

Kline, R. B. (2016). *Principles and practice of structural equation modeling* (4th ed.). Guilford Press.

Muthén, L. K., & Muthén, B. O. (1998–2017). *Mplus user's guide* (8th ed.). Muthén & Muthén.

Yuan, K.-H., & Bentler, P. M. (2000). Three likelihood-based methods for mean and covariance structures with nonnormal missing data. *Sociological Methodology, 30*(1), 165–200. https://doi.org/10.1111/0081-1750.00078

Zhao, X., Lynch, J. G., Jr., & Chen, Q. (2010). Reconsidering Baron and Kenny: Myths and truths about mediation analysis. *Journal of Consumer Research, 37*(2), 197–206. https://doi.org/10.1086/651257


*Draft generated automatically from the Mplus output. Check every statement and citation against the original sources before use.*
