import pandas as pd
from data_loader import load_energy_data


def create_features():
    df = load_energy_data()

    # Handle missing values
    df = df.fillna(method="ffill")
    df = df.fillna(
        method="bfill"
    )  # In case there are still missing values at the start
    print("Missing values after cleaning:\n", df.isnull().sum())
    # -----------------------
    # 1. Total Renewable Energy Supply
    # -----------------------

    df["renewable"] = df["solar"] + df["wind"]

    # -----------------------
    # 2. Energy Balance
    # -----------------------

    df["balance"] = df["renewable"] - df["load"]

    # -----------------------
    # 3. Demand/Supply Ratio
    # -----------------------

    df["ratio"] = df["load"] / (df["renewable"] + 1)  # Avoid division by zero

    # -----------------------
    # 4. Deficit / Surplus Flags
    # -----------------------

    df["deficit"] = df["balance"] < 0
    df["surplus"] = df["balance"] > 0

    # -----------------------
    # 5. Peak Indicator
    # -----------------------

    df["hour"] = df.index.hour
    df["is_peak"] = df["hour"].isin([8, 9, 10, 17, 18, 19])

    print(
        df[
            [
                "load",
                "solar",
                "wind",
                "renewable",
                "balance",
                "ratio",
                "deficit",
                "surplus",
                "is_peak",
            ]
        ].head()
    )
    return df


if __name__ == "__main__":
    df = create_features()
