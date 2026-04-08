# LaTeX formula strings for all mathematical content

# ==== Section 2: Harkness System ====
HARKNESS_HIGH = r"P_r = R_{avg} + 10 \times (P\% - 50)"
HARKNESS_LOW = r"P_r = R_{avg} - 10 \times (50 - P\%)"
HARKNESS_EXAMPLE = r"P_r = 2200 - 10 \times (50 - 0) = 1700"

# ==== Section 3: Elo Physics ====
PERFORMANCE_DIST = r"P \sim \mathcal{N}(\mu, \sigma^2)"
SIGMA_CALIBRATION = r"\sigma \approx 200 \text{ rating points}"
ELO_NORMAL_EXPECTED = r"E_A = \Phi\left(\frac{R_A - R_B}{\sigma\sqrt{2}}\right)"

# ==== Section 4: Logistic Elo ====
ELO_LOGISTIC = r"E_A = \frac{1}{1 + 10^{(R_B - R_A)/400}}"
ELO_UPDATE = r"R'_A = R_A + K(S_A - E_A)"
SURPRISE_FACTOR = r"\Delta = S_A - E_A"

# ==== Section 5: Facemash Error ====
FACEMASH_WRONG = r"E_A = \frac{1}{1 + 10 \times \frac{R_B - R_A}{400}}"
FACEMASH_CORRECT = r"E_A = \frac{1}{1 + 10^{(R_B - R_A)/400}}"
SYMMETRY = r"E_A + E_B = 1"

# ==== Section 7: Bayesian ====
BAYES_THEOREM = r"P(\theta|D) = \frac{P(D|\theta) \cdot P(\theta)}{P(D)}"
PRIOR = r"P(\text{skill})"
LIKELIHOOD = r"P(\text{result}|\text{skill})"
POSTERIOR = r"P(\text{skill}|\text{result})"

# ==== Section 8: Bradley-Terry ====
BTL_RATIO = r"P(i > j) = \frac{v_i}{v_i + v_j}"
BTL_LOG = r"P(i > j) = \sigma(s_i - s_j)"
SIGMOID = r"\sigma(x) = \frac{1}{1 + e^{-x}}"
HODGE = r"s_{ij} = (r_i - r_j) + \epsilon_{ij}"

# ==== Section 9: Plackett-Luce ====
PLACKETT_LUCE = r"P(\pi) = \prod_{k=1}^{n} \frac{\exp(s_{\pi_k})}{\sum_{l=k}^{n} \exp(s_{\pi_l})}"

# ==== Section 10: Hierarchical ====
LATENT_DECOMP = r"\lambda_{ijr} = \alpha_i + \beta_j + \gamma_{ij} + \epsilon_{ijr}"
CONSTRUCTOR_AR = r"\beta_j^{(t)} \sim \mathcal{N}(\beta_j^{(t-1)}, \sigma_\beta^2)"
DRIVER_PRIOR = r"\mu_{\alpha_i}^{(0)} = f(F2_i)"

# ==== Section 11: Physics/Telemetry ====
KALMAN_PREDICT = r"\hat{x}_{k|k-1} = F\hat{x}_{k-1}"
KALMAN_UPDATE = r"\hat{x}_k = \hat{x}_{k|k-1} + K_k(z_k - H\hat{x}_{k|k-1})"
KALMAN_GAIN = r"K_k = P_{k|k-1}H^T(HP_{k|k-1}H^T + R)^{-1}"
JERK = r"j(t) = \frac{da}{dt}"
BAI = r"BAI_i = \mathbb{E}[a_{brake}] - \lambda \cdot \text{Var}[j(t)]"
PACEJKA = r"F = D\sin(C\arctan(B\alpha - E(B\alpha - \arctan(B\alpha))))"
FRICTION_CIRCLE = r"F_x^2 + F_y^2 \leq (\mu N)^2"

# ==== Section 12: Survival ====
HAZARD = r"h(t) = \lim_{\Delta t \to 0} \frac{P(t \leq T < t+\Delta t | T \geq t)}{\Delta t}"
COX = r"h(t|X) = h_0(t)\exp(\beta^T X)"
IPCW_WEIGHT = r"w = \frac{1}{\hat{G}(C)}"

# ==== Section 13: MCMC ====
POSTERIOR_JOINT = r"P(\alpha, \beta | D) \propto P(D | \alpha, \beta) P(\alpha) P(\beta)"
GELMAN_RUBIN = r"\hat{R} = \sqrt{\frac{\hat{V}}{W}}"

# ==== Section 14: Volatility ====
GLICKO_RD = r"\sigma'^2 = f(\sigma'|\phi, v, \Delta)"
ENTROPY = r"H = -\sum_{i} p_i \log p_i"
ENTROPY_WEIGHT = r"w_{update} \propto e^{-H}"

# ==== Section 15: TrueSkill ====
TRUESKILL_RANK = r"R = \mu - 3\sigma"
GAUSSIAN_PRIOR = r"s \sim \mathcal{N}(\mu, \sigma^2)"

# Aliases for backwards compatibility with standalone scene files
EXPECTED_SCORE = ELO_LOGISTIC
RATING_UPDATE = ELO_UPDATE
