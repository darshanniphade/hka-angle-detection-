import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import os

# ================= SETTINGS =================
folder = r"D:\kadu sir"
output_folder = os.path.join(folder, "research_plots3")

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

plt.rcParams.update({
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.labelsize": 11
})


# ================= ICC FUNCTION =================
def calculate_icc(data):
    n, k = data.shape
    mean_per_target = np.mean(data, axis=1)
    mean_per_rater = np.mean(data, axis=0)
    grand_mean = np.mean(data)

    ss_total = np.sum((data - grand_mean)**2)
    ss_between_targets = k * np.sum((mean_per_target - grand_mean)**2)
    ss_between_raters = n * np.sum((mean_per_rater - grand_mean)**2)
    ss_error = ss_total - ss_between_targets - ss_between_raters

    ms_between_targets = ss_between_targets / (n - 1)
    ms_error = ss_error / ((n - 1) * (k - 1))

    icc = (ms_between_targets - ms_error) / \
          (ms_between_targets + (k - 1) * ms_error)

    return icc


# ================= MAIN FUNCTION =================
def research_analysis(file_name, left_col, right_col, title_prefix):

    df = pd.read_excel(os.path.join(folder, file_name),
                       usecols=[left_col, right_col])

    left = df[left_col].astype(float)
    right = df[right_col].astype(float)

    mask = ~(left.isna() | right.isna())
    left = left[mask]
    right = right[mask]

    # ================= CORRELATION =================
    r, p = stats.pearsonr(left, right)
    slope, intercept, r_val, p_val, std_err = stats.linregress(left, right)
    r2 = r_val ** 2

    plt.figure(figsize=(6,6))
    plt.scatter(left, right, alpha=0.7)

    x_line = np.linspace(min(left), max(left), 100)
    plt.plot(x_line, slope*x_line + intercept, linewidth=1.5)

    plt.xlabel("Left (cm)")
    plt.ylabel("Right (cm)")
    plt.title(f"{title_prefix} Correlation")

    eq_text = f"y = {slope:.2f}x + {intercept:.2f}\n" \
              f"r = {r:.3f}\nR² = {r2:.3f}\np = {p:.4f}"

    plt.text(0.05, 0.95, eq_text,
             transform=plt.gca().transAxes,
             verticalalignment='top',
             bbox=dict(boxstyle='round',
                       facecolor='white',
                       alpha=0.85))

    plt.tight_layout()
    plt.savefig(os.path.join(output_folder,
                f"{title_prefix}_correlation.png"), dpi=300)
    plt.close()

    # ================= ICC =================
    icc_value = calculate_icc(np.vstack((left, right)).T)

    # ================= BLAND–ALTMAN =================
    mean = (left + right) / 2
    diff = right - left

    bias = np.mean(diff)
    sd = np.std(diff, ddof=1)

    upper = bias + 1.96 * sd
    lower = bias - 1.96 * sd

    n = len(diff)
    se_bias = sd / np.sqrt(n)
    ci_upper = bias + 1.96 * se_bias
    ci_lower = bias - 1.96 * se_bias

    shapiro_stat, shapiro_p = stats.shapiro(diff)

    plt.figure(figsize=(8,6))
    plt.scatter(mean, diff, alpha=0.7)

    plt.axhline(bias, color='black', linewidth=1.5)
    plt.axhline(upper, linestyle='--', linewidth=1.5)
    plt.axhline(lower, linestyle='--', linewidth=1.5)

    plt.xlabel("Mean (cm)")
    plt.ylabel("Difference (Right - Left) (cm)")
    plt.title(f"{title_prefix} Bland–Altman")

    # Shift line labels slightly outside data cloud
    x_text = min(mean) - 0.5

    plt.text(x_text, upper, f"+1.96 SD: {upper:.2f}",
             va='bottom')

    plt.text(x_text, bias, f"Mean diff: {bias:.2f}",
             va='bottom')

    plt.text(x_text, lower, f"-1.96 SD: {lower:.2f}",
             va='top')

    # Statistics box placed safely in upper-left empty region
    textstr = '\n'.join((
        f'+1.96 SD: {upper:.2f}',
        f'Mean diff: {bias:.2f}',
        f'-1.96 SD: {lower:.2f}',
        f'95% CI bias: [{ci_lower:.2f}, {ci_upper:.2f}]',
        f'Shapiro p: {shapiro_p:.4f}'
    ))

    plt.text(0.02, 0.98, textstr,
             transform=plt.gca().transAxes,
             verticalalignment='top',
             bbox=dict(boxstyle='round',
                       facecolor='white',
                       alpha=0.9))

    plt.tight_layout()
    plt.savefig(os.path.join(output_folder,
                f"{title_prefix}_bland_altman.png"), dpi=300)
    plt.close()

    # ================= HISTOGRAM =================
    plt.figure(figsize=(6,5))
    plt.hist(diff, bins=10, density=True, alpha=0.6)

    mu, sigma = stats.norm.fit(diff)
    x = np.linspace(min(diff), max(diff), 100)
    plt.plot(x, stats.norm.pdf(x, mu, sigma), linewidth=2)

    plt.xlabel("Difference (cm)")
    plt.ylabel("Density")
    plt.title(f"{title_prefix} Difference Distribution")

    plt.tight_layout()
    plt.savefig(os.path.join(output_folder,
                f"{title_prefix}_histogram.png"), dpi=300)
    plt.close()

    # ================= BOXPLOT =================
    plt.figure(figsize=(6,5))
    plt.boxplot([left, right], labels=["Left", "Right"])
    plt.ylabel("Length (cm)")
    plt.title(f"{title_prefix} Boxplot")

    plt.tight_layout()
    plt.savefig(os.path.join(output_folder,
                f"{title_prefix}_boxplot.png"), dpi=300)
    plt.close()

    # ================= PRINT SUMMARY =================
    print(f"\n===== {title_prefix} =====")
    print(f"Pearson r: {r:.4f}")
    print(f"R²: {r2:.4f}")
    print(f"p-value: {p:.6f}")
    print(f"ICC(3,1): {icc_value:.4f}")
    print(f"Bias: {bias:.4f}")
    print(f"Upper LOA: {upper:.4f}")
    print(f"Lower LOA: {lower:.4f}")
    print(f"95% CI Bias: [{ci_lower:.4f}, {ci_upper:.4f}]")
    print(f"Shapiro p-value: {shapiro_p:.6f}")
    print("="*40)


# ================= RUN FOR ALL =================

research_analysis(
    "Femur length right leg Vs left leg .xlsx",
    "Left_Femur Length in cm",
    "Right_Femur Length in cm",
    "Femur"
)

research_analysis(
    "Tibia length right leg Vs left leg .xlsx",
    "tibi_l_cm",
    "tibia_r_cm",
    "Tibia"
)

research_analysis(
    "leg length right leg Vs left leg .xlsx",
    "height_l_cm",
    "height_r_cm",
    "Leg_Length"
)

print("\nAll research plots saved in:", output_folder)