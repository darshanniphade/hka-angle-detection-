import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import os

folder = r"D:\kadu sir"
output_folder = os.path.join(folder, "research_plots")

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def research_analysis(file_name, left_col, right_col, title_prefix):

    df = pd.read_excel(os.path.join(folder, file_name),
                       usecols=[left_col, right_col])

    left = df[left_col].astype(float)
    right = df[right_col].astype(float)

    # ---------------- CORRELATION ----------------
    r, p = stats.pearsonr(left, right)
    slope, intercept, r_val, p_val, std_err = stats.linregress(left, right)
    r2 = r_val**2

    # Scatter + Regression
    plt.figure()
    plt.scatter(left, right)
    x_line = np.linspace(min(left), max(left), 100)
    plt.plot(x_line, slope*x_line + intercept)
    plt.xlabel("Left (cm)")
    plt.ylabel("Right (cm)")
    plt.title(f"{title_prefix} Scatter\nr={r:.3f}, R²={r2:.3f}")
    plt.savefig(os.path.join(output_folder, f"{title_prefix}_scatter.png"), dpi=300)
    plt.close()

    # ---------------- BLAND-ALTMAN ----------------
    mean = (left + right) / 2
    diff = right - left
    bias = np.mean(diff)
    sd = np.std(diff, ddof=1)
    upper = bias + 1.96 * sd
    lower = bias - 1.96 * sd

    plt.figure()
    plt.scatter(mean, diff)
    plt.axhline(bias, linestyle="--")
    plt.axhline(upper, linestyle="--")
    plt.axhline(lower, linestyle="--")
    plt.xlabel("Mean (cm)")
    plt.ylabel("Difference (Right - Left) (cm)")
    plt.title(f"{title_prefix} Bland-Altman")
    plt.savefig(os.path.join(output_folder, f"{title_prefix}_bland_altman.png"), dpi=300)
    plt.close()

    # ---------------- HISTOGRAM ----------------
    plt.figure()
    plt.hist(diff, bins=10)
    plt.xlabel("Difference (cm)")
    plt.title(f"{title_prefix} Difference Distribution")
    plt.savefig(os.path.join(output_folder, f"{title_prefix}_histogram.png"), dpi=300)
    plt.close()

    # ---------------- BOXPLOT ----------------
    plt.figure()
    plt.boxplot([left, right], labels=["Left", "Right"])
    plt.title(f"{title_prefix} Boxplot")
    plt.ylabel("Length (cm)")
    plt.savefig(os.path.join(output_folder, f"{title_prefix}_boxplot.png"), dpi=300)
    plt.close()

    print(f"---- {title_prefix} ----")
    print(f"Pearson r: {r:.4f}")
    print(f"p-value: {p:.6f}")
    print(f"R²: {r2:.4f}")
    print(f"Bias: {bias:.4f}")
    print(f"Upper LOA: {upper:.4f}")
    print(f"Lower LOA: {lower:.4f}")
    print("-" * 40)


# ================== RUN FOR ALL ==================

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

print("All research plots saved in:", output_folder)