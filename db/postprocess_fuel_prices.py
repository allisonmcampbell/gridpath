"""
Post-processing script: deduplicate fuel prices (Oil duplicates).

Run from db/ after gridpath_run_data_toolkit (step 4) and before
gridpath_create_database (step 5). Must be re-run every time step 4
regenerates the CSVs.

Why: Multiple AEO fuel types map to the same GridPath "Oil" fuel name,
producing duplicate (fuel, period, month) rows. The UNIQUE constraint on
inputs_fuel_prices rejects them. We keep the highest-price (non-zero) row.
"""

import pandas as pd

path = "./csvs_ra_toolkit_e2e/fuels/fuel_prices/1_aeo2022.csv"
df = pd.read_csv(path)
before = len(df)
df = (
    df.sort_values("fuel_price_per_mmbtu", ascending=False)
    .drop_duplicates(subset=["fuel", "period", "month"], keep="first")
    .sort_values(["fuel", "period", "month"])
    .reset_index(drop=True)
)
print(f"Fuel prices: {before} -> {len(df)} (removed {before - len(df)})")
df.to_csv(path, index=False)
