#!/usr/bin/env python
"""Vendor 2FA compliance checker for DME.

Usage:
    python scripts/vendor_2fa_compliance_check.py path/to/DME_Vendor_list.xlsx

The script expects a sheet with (at minimum) the following columns:

- Vendor Name
- Status
- 2FA Enabled (Yes/No)

It will:
- Filter rows where Status = 'Active'
- Check if '2FA Enabled (Yes/No)' is 'Yes' (case-insensitive)
- Print a summary
- Write 'vendor_2fa_gaps.csv' if any Active vendors are missing 2FA
"""

import sys
import os
import pandas as pd


REQUIRED_COLUMNS = [
    "Vendor Name",
    "Status",
    "2FA Enabled (Yes/No)",
]


def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/vendor_2fa_compliance_check.py path/to/vendor_list.xlsx")
        sys.exit(1)

    path = sys.argv[1]
    if not os.path.exists(path):
        print(f"File not found: {path}")
        sys.exit(1)

    df = pd.read_excel(path)

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        print("Error: Missing required columns:", ", ".join(missing))
        print("Available columns:", ", ".join(df.columns))
        sys.exit(1)

    # Normalise values
    df["Status_norm"] = df["Status"].astype(str).str.strip().str.lower()
    df["TwoFA_norm"] = df["2FA Enabled (Yes/No)"].astype(str).str.strip().str.lower()

    active = df[df["Status_norm"] == "active"]
    gaps = active[active["TwoFA_norm"] != "yes"]

    total_active = len(active)
    gaps_count = len(gaps)

    print(f"Total vendors with Status='Active': {total_active}")
    print(f"Active vendors with 2FA != 'Yes': {gaps_count}")

    if gaps_count > 0:
        out_path = "vendor_2fa_gaps.csv"
        gaps.to_csv(out_path, index=False)
        print(f"WARNING: 2FA gaps found. Details written to {out_path}")
    else:
        print("All Active vendors have 2FA Enabled = 'Yes' (according to the sheet).")


if __name__ == "__main__":
    main()
