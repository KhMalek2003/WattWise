import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from data_loader import load_energy_data


def run_eda():
    df = load_energy_data()

    # Handle missing values
    df = df.fillna(method="ffill")
    print("Missing values after cleaning:\n", df.isnull().sum())

    # -------------------------------
    # 1. Time series plot
    # -------------------------------

    plt.figure(figsize=(15, 5))
    plt.plot(df.index, df["load"], label="Load")
    plt.plot(df.index, df["solar"], label="Solar")
    plt.plot(df.index, df["wind"], label="Wind")
    plt.title("Energy Time Series")
    plt.legend()
    plt.show()

    # -------------------------------
    # 2. Daily Patterns (Average by hour)
    # -------------------------------

    df["hour"] = df.index.hour
    hourly_avg = df.groupby("hour").mean()
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=hourly_avg)
    plt.title("Average Daily Patterns")
    plt.show()

    # -------------------------------
    # 2. Correlation
    # -------------------------------

    plt.figure(figsize=(6, 4))
    sns.heatmap(df[["load", "solar", "wind"]].corr(), annot=True, cmap="coolwarm")
    plt.title("Correlation Matrix")
    plt.show()

    # -------------------------------
    # 4. Distribution of Load
    # -------------------------------

    df[["load", "solar", "wind"]].hist(bins=50, figsize=(12, 6))
    plt.suptitle("Distribution")
    plt.show()

    # -------------------------------
    # 5. Rolling Average
    # -------------------------------
    df["load_rolling"] = df["load"].rolling(window=24).mean()
    plt.figure(figsize=(15, 5))
    plt.plot(df.index, df["load"], alpha=0.3, label="Original Load")
    plt.plot(df.index, df["load_rolling"], color="red", label="24-Hour Rolling Average")
    plt.title("Load with Rolling Average")
    plt.legend()
    plt.show()
    # -------------------------------
    # 6. Trend Analysis (Monthly)
    # -------------------------------
    monthly_avg = df.resample("M").mean()
    plt.figure(figsize=(12, 5))
    plt.plot(monthly_avg.index, monthly_avg["load"], label="Load Trend")
    plt.plot(monthly_avg.index, monthly_avg["solar"], label="Solar Trend")
    plt.plot(monthly_avg.index, monthly_avg["wind"], label="Wind Trend")
    plt.title("Monthly Energy Trends")
    plt.legend()
    plt.show()
    # -------------------------------
    # 7. Risk Detection
    # -------------------------------
    df["risk"] = df["load"] - (df["solar"] + df["wind"])
    plt.figure(figsize=(15, 5))
    plt.plot((df.index), df["risk"], label="Energy Deficit(Risk)")
    plt.title("Energy Risk (Demand - Renewable Supply)")
    plt.legend()
    plt.show()
    # -------------------------------
    # 8. Identify High Risk Periods
    # -------------------------------
    high_risk = df[df["risk"] > df["risk"].quantile(0.9)]
    print("\n High Risk periods:")
    print(high_risk[["load", "solar", "wind", "risk"]].head())


if __name__ == "__main__":
    run_eda()
