import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# File paths
left_path = r"D:\kadu sir\HKA left leg Vs Radiologist .xlsx"
right_path = r"D:\kadu sir\HKA right leg Vs Radiologist.xlsx"

def bland_altman(model, radiologist, title):
    mean = (model + radiologist) / 2
    diff = model - radiologist

    bias = np.mean(diff)
    sd = np.std(diff, ddof=1)

    upper = bias + 1.96 * sd
    lower = bias - 1.96 * sd

    plt.figure(figsize=(8,6))
    plt.scatter(mean, diff, alpha=0.7)

    plt.axhline(bias, linestyle="--", label=f"Bias = {bias:.2f}")
    plt.axhline(upper, linestyle="--", label=f"+1.96 SD = {upper:.2f}")
    plt.axhline(lower, linestyle="--", label=f"-1.96 SD = {lower:.2f}")

    plt.title(title)
    plt.xlabel("Mean of Model and Radiologist (°)")
    plt.ylabel("Difference (Model − Radiologist) (°)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.show()

    print(title)
    print(f"Bias: {bias:.3f}")
    print(f"Upper Limit: {upper:.3f}")
    print(f"Lower Limit: {lower:.3f}")
    print("-" * 50)


# ---------------- LEFT LEG ----------------
left_df = pd.read_excel(left_path, usecols=["hka_l", "Radiologist"])
bland_altman(
    left_df["hka_l"],
    left_df["Radiologist"],
    "Bland–Altman Plot: Model vs Radiologist (Left Leg)"
)

# ---------------- RIGHT LEG ----------------
right_df = pd.read_excel(right_path, usecols=["hka_right", "Radiologist"])
bland_altman(
    right_df["hka_right"],
    right_df["Radiologist"],
    "Bland–Altman Plot: Model vs Radiologist (Right Leg)"
)