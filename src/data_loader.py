from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA_PATH = PROJECT_ROOT / "data" / "time_series_60min_singleindex.csv"


def load_energy_data(path=None):
    csv_path = Path(path) if path is not None else DEFAULT_DATA_PATH
    if not csv_path.is_absolute():
        csv_path = (PROJECT_ROOT / csv_path).resolve()

    df = pd.read_csv(csv_path)

    # Convert utc_timestamp columns into pandas datetime objects(from txt to pandas datetime values)
    df["utc_timestamp"] = pd.to_datetime(df["utc_timestamp"])

    # Set time as index for time series analysis
    df = df.set_index("utc_timestamp")

    # Keep only Germany energy dataset
    columns_to_keep = [
        "DE_load_actual_entsoe_transparency",
        "DE_solar_generation_actual",
        "DE_wind_onshore_generation_actual",
    ]
    df = df[columns_to_keep]
    # Rename columns for Simplicity
    df = df.rename(
        columns={
            "DE_load_actual_entsoe_transparency": "load",
            "DE_solar_generation_actual": "solar",
            "DE_wind_onshore_generation_actual": "wind",
        }
    )

    return df


if __name__ == "__main__":
    df = load_energy_data()

    print("Shape of the dataset:", df.shape)
    print("\nCloumns:", df.columns)
    print("\nData types:\n", df.dtypes)
    print("\nFirst 5 rows:\n", df.head())
    print("\nMissing values:\n", df.isnull().sum())
    print("\nStatistical summary:\n", df.describe())
