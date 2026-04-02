from feature_engineering import create_features
from optimization import run_optimization


def run_scenarios():

    # -------------------------------
    # Scenario 1: Normal
    # -------------------------------
    print("\n--- Scenario 1: Normal ---")
    df = create_features()
    run_optimization(df)

    # -------------------------------
    # Scenario 2: Low Solar
    # -------------------------------
    print("\n--- Scenario 2: Low Solar ---")
    df = create_features()
    df["solar"] *= 0.3
    df["renewable"] = df["solar"] + df["wind"]

    run_optimization(df)

    # -------------------------------
    # Scenario 3: High Demand
    # -------------------------------
    print("\n--- Scenario 3: High Demand ---")
    df = create_features()
    df["load"] *= 1.3

    run_optimization(df)


if __name__ == "__main__":
    run_scenarios()
