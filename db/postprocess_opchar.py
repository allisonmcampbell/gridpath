"""
Post-processing script: fix opchar scenario IDs and null missing fuel references.

Run from db/ after gridpath_run_data_toolkit (step 4) and before
gridpath_create_database (step 5). Must be re-run every time step 4
regenerates the CSVs.

Why: The opchar script assigns default sub-subscenario ID=1 for all types,
but the e2e config uses hydro ID=5 and var gen ID=3. Also, 56 biomass/nuclear
projects get fuel_scenario_id=1 but the fuel script skips them (no AEO region
mapping), causing FK failures at DB load.
"""

import os
import pandas as pd

path = "./csvs_ra_toolkit_e2e/project/opchar/1_ra_toolkit_e2e.csv"
df = pd.read_csv(path)

mask_h = df["hydro_operational_chars_scenario_id"].notna()
df.loc[mask_h, "hydro_operational_chars_scenario_id"] = 5

mask_v = df["variable_generator_profile_scenario_id"].notna()
df.loc[mask_v, "variable_generator_profile_scenario_id"] = 3

fuel_dir = "./csvs_ra_toolkit_e2e/project/opchar/fuels/"
fuel_projects = set(f.split("-")[0] for f in os.listdir(fuel_dir) if f.endswith(".csv"))
mask_f = (df["project_fuel_scenario_id"].notna()) & (~df["project"].isin(fuel_projects))
df.loc[mask_f, "project_fuel_scenario_id"] = None

print(f"Fixed hydro={mask_h.sum()}, vargen={mask_v.sum()}, fuel={mask_f.sum()}")
df.to_csv(path, index=False)
