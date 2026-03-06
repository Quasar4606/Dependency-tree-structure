import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("results/results_depth.csv")

grouped = df.groupby("length").agg({
    "real_depth": ["mean", "count"],
    "random_depth": "mean"
})

# flatten column names
grouped.columns = ["real_mean", "count", "random_mean"]

# remove noisy tail (lengths with very few sentences)
grouped = grouped[grouped["count"] >= 20]

plt.plot(grouped.index, grouped["real_mean"], label="Real")
plt.plot(grouped.index, grouped["random_mean"], label="Random")

plt.xlabel("Sentence length")
plt.ylabel("Average tree depth")
plt.legend()

plt.savefig("results/depth_curve.png")
plt.show()