# FINAL CLASS PROJECT SEM (mediation)


## Analysis

Analyses were conducted in Mplus 9.1.1 (Muthén & Muthén, 1998–2017) using MLR estimation with robust standard errors (Yuan & Bentler, 2000). The analysis included N = 1,563 observations.


## Model fit

The model showed the following fit: χ²(57) = 274.77, p < .001, CFI = .968, TLI = .957, RMSEA = .049 (90% CI [.044, .055]), SRMR = .040. The chi-square value is a scaled (robust) statistic. CFI and TLI were both good (≥ .95 indicates good fit, ≥ .90 acceptable) (Hu & Bentler, 1999; Kline, 2016). RMSEA was good (≤ .06 good, ≤ .08 acceptable) (Hu & Bentler, 1999; Browne & Cudeck, 1993), and SRMR was good (≤ .08) (Hu & Bentler, 1999). The chi-square test was significant, which is common in large samples and is usually interpreted alongside approximate fit indices (Kline, 2016). Overall, the model fit the data well.

**Table 1. Model fit indices**

| Index | Value |
|---|---|
| χ² (df) | 274.77 (57) |
| p | < .001 |
| CFI | .968 |
| TLI | .957 |
| RMSEA [90% CI] | .049 [.044, .055] |
| SRMR | .040 |


## Measurement model

For perceived disciplinary climate, standardized loadings ranged from .611 to .916. For student behavior stress, standardized loadings ranged from .398 to .929; TT3G52F fell below .50. For classroom management self-efficacy, standardized loadings ranged from .654 to .812. Loadings of .50 or higher are generally considered adequate and .70 or higher strong (Hair et al., 2019).

**Table 2. Standardized factor loadings**

| Factor | Item | β | SE | p |
|---|---|---|---|---|
| Perceived disciplinary climate | TT3G41A | .756 | .017 | — (fixed) |
| Perceived disciplinary climate | TT3G41BR | .611 | .024 | < .001 |
| Perceived disciplinary climate | TT3G41C | .916 | .009 | < .001 |
| Perceived disciplinary climate | TT3G41D | .894 | .009 | < .001 |
| Student behavior stress | TT3G52F | .398 | .024 | — (fixed) |
| Student behavior stress | TT3G52G | .929 | .023 | < .001 |
| Student behavior stress | TT3G52H | .589 | .028 | < .001 |
| Classroom management self-efficacy | TT3G34D | .808 | .014 | — (fixed) |
| Classroom management self-efficacy | TT3G34F | .654 | .021 | < .001 |
| Classroom management self-efficacy | TT3G34H | .812 | .015 | < .001 |
| Classroom management self-efficacy | TT3G34I | .740 | .016 | < .001 |


## Structural model

Perceived disciplinary climate positively predicted student behavior stress (β = .604, p < .001). Student behavior stress negatively predicted classroom management self-efficacy (β = -.217, p < .001). Perceived disciplinary climate negatively predicted classroom management self-efficacy (β = -.180, p < .001). Gender (recoded) negatively predicted student behavior stress (β = -.084, p = .001). Years of teaching experience negatively predicted student behavior stress (β = -.058, p = .010). Gender (recoded) negatively predicted classroom management self-efficacy (β = -.106, p < .001). Years of teaching experience positively predicted classroom management self-efficacy (β = .090, p = .001). Variance explained: student behavior stress R² = .385; classroom management self-efficacy R² = .158.

**Table 4. Structural paths**

| Path | B | β | SE (β) | p |
|---|---|---|---|---|
| perceived disciplinary climate → student behavior stress | .396 | .604 | .027 | < .001 |
| student behavior stress → classroom management self-efficacy | -.318 | -.217 | .037 | < .001 |
| perceived disciplinary climate → classroom management self-efficacy | -.173 | -.180 | .039 | < .001 |
| gender (recoded) → student behavior stress | -.071 | -.084 | .024 | .001 |
| years of teaching experience → student behavior stress | -.023 | -.058 | .022 | .010 |
| gender (recoded) → classroom management self-efficacy | -.130 | -.106 | .027 | < .001 |
| years of teaching experience → classroom management self-efficacy | .053 | .090 | .027 | .001 |


## Indirect effects

The standardized indirect effect of perceived disciplinary climate on classroom management self-efficacy was β = -.131 (SE = .023, p < .001), the direct effect was β = -.180 (p < .001), and the total effect was β = -.312 (p < .001). This pattern is consistent with complementary mediation (indirect and direct effects share a sign) (Zhao et al., 2010). Indirect effects here were tested with the delta method; bootstrapped confidence intervals are generally recommended where available (Hayes, 2018).

**Table 5. Standardized direct, indirect and total effects**

| Effect | Direct | Indirect | Total |
|---|---|---|---|
| perceived disciplinary climate → classroom management self-efficacy | -.180 (p< .001) | -.131 (p< .001) | -.312 (p< .001) |


## Notes from Mplus to check

- Mplus reported that standard errors may not be trustworthy for some parameters (possible non-identification).

## References

Browne, M. W., & Cudeck, R. (1993). Alternative ways of assessing model fit. In K. A. Bollen & J. S. Long (Eds.), *Testing structural equation models* (pp. 136–162). Sage.

Hair, J. F., Black, W. C., Babin, B. J., & Anderson, R. E. (2019). *Multivariate data analysis* (8th ed.). Cengage.

Hayes, A. F. (2018). *Introduction to mediation, moderation, and conditional process analysis: A regression-based approach* (2nd ed.). Guilford Press.

Hu, L., & Bentler, P. M. (1999). Cutoff criteria for fit indexes in covariance structure analysis: Conventional criteria versus new alternatives. *Structural Equation Modeling, 6*(1), 1–55. https://doi.org/10.1080/10705519909540118

Kline, R. B. (2016). *Principles and practice of structural equation modeling* (4th ed.). Guilford Press.

Muthén, L. K., & Muthén, B. O. (1998–2017). *Mplus user's guide* (8th ed.). Muthén & Muthén.

Yuan, K.-H., & Bentler, P. M. (2000). Three likelihood-based methods for mean and covariance structures with nonnormal missing data. *Sociological Methodology, 30*(1), 165–200. https://doi.org/10.1111/0081-1750.00078

Zhao, X., Lynch, J. G., Jr., & Chen, Q. (2010). Reconsidering Baron and Kenny: Myths and truths about mediation analysis. *Journal of Consumer Research, 37*(2), 197–206. https://doi.org/10.1086/651257


*Draft generated automatically from the Mplus output. Check every statement and citation against the original sources before use.*
