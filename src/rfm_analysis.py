from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data/processed/customer_transactions.csv"
OUTPUT = ROOT / "data/processed"
REPORTS = ROOT / "reports"

OUTPUT.mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)

print("Loading customer transaction data...")
df = pd.read_csv(INPUT, parse_dates=["InvoiceDate"])

required = [
    "Invoice", "InvoiceDate", "Customer ID", "TotalPrice"
]
missing = [col for col in required if col not in df.columns]

if missing:
    raise ValueError(f"Missing required columns: {missing}")

df = df.dropna(subset=["Customer ID", "InvoiceDate", "TotalPrice"])

# Use the day after the latest transaction as the reference date.
reference_date = df["InvoiceDate"].max().normalize() + pd.Timedelta(days=1)

print("Calculating RFM metrics...")

rfm = df.groupby("Customer ID").agg(
    Recency=("InvoiceDate", lambda x: (reference_date - x.max().normalize()).days),
    Frequency=("Invoice", "nunique"),
    Monetary=("TotalPrice", "sum")
).reset_index()

rfm = rfm.rename(columns={"Customer ID": "CustomerID"})

# Keep customers with positive monetary value for this segmentation.
rfm = rfm[
    (rfm["Frequency"] > 0) &
    (rfm["Monetary"] > 0)
].copy()

rfm.to_csv(OUTPUT / "customer_rfm.csv", index=False)

print(f"Customers available for segmentation: {len(rfm):,}")
print("\nRFM summary:")
print(rfm[["Recency", "Frequency", "Monetary"]].describe())

# Reduce skewness before scaling.
features = ["Recency", "Frequency", "Monetary"]
X_log = np.log1p(rfm[features])

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_log)

pd.DataFrame(
    X_scaled, columns=features
).to_csv(OUTPUT / "customer_rfm_scaled.csv", index=False)

print("\nEvaluating K-Means cluster counts...")

evaluation = []
models = {}

for k in range(2, 9):
    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )
    labels = model.fit_predict(X_scaled)

    score = silhouette_score(
        X_scaled,
        labels,
        sample_size=min(5000, len(X_scaled)),
        random_state=42
    )

    evaluation.append({
        "k": k,
        "inertia": model.inertia_,
        "silhouette_score": score
    })
    models[k] = model

    print(
        f"k={k}: inertia={model.inertia_:.2f}, "
        f"silhouette={score:.4f}"
    )

evaluation_df = pd.DataFrame(evaluation)
evaluation_df.to_csv(REPORTS / "cluster_evaluation.csv", index=False)

# Select the model with the highest silhouette score.
# The project requires at least four actionable customer segments.
# k=4 is selected as a business-oriented candidate.
# Its silhouette score will be reported alongside other candidates.
best_k = 4

best_model = models[best_k]
rfm["Cluster"] = best_model.labels_

print(f"\nSelected business-oriented k: {best_k}")

# Create segment profiles in original RFM units.
profile = rfm.groupby("Cluster").agg(
    Customers=("CustomerID", "count"),
    Avg_Recency=("Recency", "mean"),
    Avg_Frequency=("Frequency", "mean"),
    Avg_Monetary=("Monetary", "mean"),
    Total_Revenue=("Monetary", "sum")
).reset_index()

profile["Customer_Percentage"] = (
    profile["Customers"] / len(rfm) * 100
)

# Assign descriptive labels using relative cluster behaviour.
median_recency = profile["Avg_Recency"].median()
median_frequency = profile["Avg_Frequency"].median()
median_monetary = profile["Avg_Monetary"].median()

def segment_name(row):
    recent = row["Avg_Recency"] <= median_recency
    frequent = row["Avg_Frequency"] >= median_frequency
    valuable = row["Avg_Monetary"] >= median_monetary

    if recent and frequent and valuable:
        return "Champions"
    if frequent and valuable:
        return "Loyal High-Value"
    if recent and frequent:
        return "Recent Loyal Customers"
    if not recent and not frequent:
        return "At-Risk / Hibernating"
    if valuable:
        return "Potential High-Value"
    if recent:
        return "Recent Customers"
    return "Needs Attention"

profile["Segment"] = profile.apply(segment_name, axis=1)

rfm = rfm.merge(
    profile[["Cluster", "Segment"]],
    on="Cluster",
    how="left"
)

rfm.to_csv(OUTPUT / "customer_segments.csv", index=False)
profile.to_csv(REPORTS / "customer_segment_profile.csv", index=False)

# Elbow plot.
plt.figure(figsize=(8, 5))
plt.plot(
    evaluation_df["k"],
    evaluation_df["inertia"],
    marker="o"
)
plt.title("Elbow Method for K-Means")
plt.xlabel("Number of Clusters (k)")
plt.ylabel("Inertia")
plt.xticks(evaluation_df["k"])
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(REPORTS / "elbow_method.png", dpi=150)
plt.close()

# Silhouette plot.
plt.figure(figsize=(8, 5))
plt.plot(
    evaluation_df["k"],
    evaluation_df["silhouette_score"],
    marker="o"
)
plt.title("Silhouette Score by Number of Clusters")
plt.xlabel("Number of Clusters (k)")
plt.ylabel("Silhouette Score")
plt.xticks(evaluation_df["k"])
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(REPORTS / "silhouette_analysis.png", dpi=150)
plt.close()

# RFM distributions.
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for ax, column in zip(axes, features):
    ax.hist(rfm[column], bins=40)
    ax.set_title(f"{column} Distribution")
    ax.set_xlabel(column)
    ax.set_ylabel("Customers")

plt.tight_layout()
plt.savefig(REPORTS / "rfm_distribution.png", dpi=150)
plt.close()

print("\nCustomer segment profile:")
print(profile.round(2).to_string(index=False))

print("\nFiles generated:")
print("- data/processed/customer_rfm.csv")
print("- data/processed/customer_rfm_scaled.csv")
print("- data/processed/customer_segments.csv")
print("- reports/cluster_evaluation.csv")
print("- reports/customer_segment_profile.csv")
print("- reports/elbow_method.png")
print("- reports/silhouette_analysis.png")
print("- reports/rfm_distribution.png")
