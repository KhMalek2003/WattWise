import pandas as pd
from feature_engineering import create_features


def run_optimization(df=None):
    if df is None:
        df = create_features()

    # --------------------------------
    # Battery Configuration
    # --------------------------------
    battery_capacity = 10000  # max storage (Mwh)
    battery_level = 0  # current storage (Mwh)
    battery_levels = []
    actions = []
    grid_supplies = []
    total_supplies = []

    for i, row in df.iterrows():
        renewable = row["renewable"]
        load = row["load"]

        # Simulate grid backup (gas plants, nuclear, hydro,core)

        max_grid_capacity = 50000  # max backup power
        response_factor = (
            0.8  # how much of the needed power can be supplied by the grid
        )
        reserve_margin = 10000  # extra production buffer
        needed = load - renewable + reserve_margin
        if needed > 0:
            grid_supply = min(needed * response_factor, max_grid_capacity)
        else:
            grid_supply = 0

        total_supply = renewable + grid_supply
        balance = total_supply - load
        df.at[i, "balance"] = balance  # Store balance as the total supply - load

        # --------------------------------
        # Case 1: Surplus -> Store energy
        # --------------------------------
        if balance > 0:
            charge = min(balance, battery_capacity - battery_level)
            battery_level += charge
            action = "store"

        # --------------------------------
        # Case 2: Deficit -> Use Battery
        # --------------------------------
        elif balance < 0:
            discharge = min(abs(balance), battery_level)
            battery_level -= discharge
            action = "use_battery"

        else:
            action = "idle"

        grid_supplies.append(grid_supply)
        total_supplies.append(total_supply)
        battery_levels.append(battery_level)
        actions.append(action)

    df["grid_supply"] = grid_supplies
    df["total_supply"] = total_supplies
    df["battery_level"] = battery_levels
    df["action"] = actions

    print(
        df[
            [
                "grid_supply",
                "renewable",
                "total_supply",
                "load",
                "balance",
                "battery_level",
                "action",
            ]
        ].head(20)
    )

    return df


if __name__ == "__main__":
    run_optimization()
