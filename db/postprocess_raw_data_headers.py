"""
Post-processing script: rename raw data CSV headers to match v2026 schema.

Run from db/ after downloading PUDL and RA Toolkit data (steps 2-3) and before
running the data toolkit (step 4). Only needs to run once per download, but is
safe to re-run (idempotent).

Why: The PUDL extraction and RA Toolkit download produce CSVs with column names
from the v2025 schema (load_zone_unit, load_mw, cap_factor). The v2026 data
toolkit expects the renamed columns (unit, value).
"""

import pandas as pd
import os
import sys

raw_data_dir = os.path.join("..", "raw_data")

renames = [
    {
        "file": "ra_toolkit_load.csv",
        "columns": {"load_zone_unit": "unit", "load_mw": "value"},
    },
    {
        "file": "pudl_ra_toolkit_var_profiles.csv",
        "columns": {"cap_factor": "value"},
    },
]

for spec in renames:
    path = os.path.join(raw_data_dir, spec["file"])
    if not os.path.exists(path):
        print(f"SKIP {spec['file']} (not found)")
        continue

    df = pd.read_csv(path, nrows=0)
    cols_to_rename = {k: v for k, v in spec["columns"].items() if k in df.columns}

    if not cols_to_rename:
        already = all(v in df.columns for v in spec["columns"].values())
        if already:
            print(f"OK   {spec['file']} (headers already correct)")
        else:
            print(
                f"WARN {spec['file']} (expected columns not found: {list(spec['columns'].keys())})"
            )
        continue

    df = pd.read_csv(path)
    df = df.rename(columns=cols_to_rename)
    df.to_csv(path, index=False)
    print(f"FIXED {spec['file']}: renamed {cols_to_rename}")
