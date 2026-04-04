from src.feature_engineering import create_features


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
    balances = []
    battery_flows = []

    for i, renewable, load in zip(
        df.index, df["renewable"].to_numpy(), df["load"].to_numpy()
    ):
        # Simulate grid backup (gas plants, nuclear, hydro,core)

        max_grid_capacity = 50000  # max backup power
        raw_balance = renewable - load
        grid_supply = 0
        battery_flow = 0

        # --------------------------------
        # Case 1: Surplus renewable -> Store energy(charge battery)
        # --------------------------------
        if raw_balance > 0:
            charge = min(raw_balance, battery_capacity - battery_level)
            battery_level += charge
            battery_flow = charge
            action = "store"

        # --------------------------------
        # Case 2: Deficit -> Use Battery
        # --------------------------------
        elif raw_balance < 0:
            deficit = abs(raw_balance)
            discharge = min(deficit, battery_level)
            battery_level -= discharge
            battery_flow = -discharge
            remaining_deficit = deficit - discharge
            grid_supply = min(remaining_deficit, max_grid_capacity)

            if discharge > 0:
                action = "use_battery"
            elif grid_supply > 0:
                action = "use_grid"
            else:
                action = "unserved"

        else:
            action = "idle"

        battery_discharge = max(-battery_flow, 0)

        total_supply = renewable + grid_supply + battery_discharge
        balance = total_supply - load

        grid_supplies.append(grid_supply)
        total_supplies.append(total_supply)
        balances.append(balance)
        battery_levels.append(battery_level)
        battery_flows.append(battery_flow)
        actions.append(action)

    df["grid_supply"] = grid_supplies
    df["total_supply"] = total_supplies
    df["balance"] = balances
    df["battery_level"] = battery_levels
    df["battery_flow"] = battery_flows
    df["action"] = actions

    return df


if __name__ == "__main__":
    run_optimization()
