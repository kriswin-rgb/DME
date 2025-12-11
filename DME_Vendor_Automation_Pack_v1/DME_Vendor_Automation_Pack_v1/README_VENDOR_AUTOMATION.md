# DME Vendor & Automation Pack v1

This mini-pack is designed to drop into your main DME repo.

## Structure

- `docs/DME_Vendor_Identity_Automation_DevOps_101_v1_1.md`  
  Extended DevOps 101 covering vendors, identity, email, automation, and secrets.

- `scripts/vendor_2fa_compliance_check.py`  
  Helper script to audit your Master Vendor List Excel for missing 2FA on Active vendors.

## Suggested repo placement

Drop the contents into your existing repo:

- `docs/` → merge with existing docs.
- `scripts/` → merge with your scripts folder (or create it).

## Usage: vendor_2fa_compliance_check.py

From the repo root:

```bash
python scripts/vendor_2fa_compliance_check.py DME_Vendor_list.xlsx
```

- The script prints a summary to stdout.
- If gaps are found, it writes `vendor_2fa_gaps.csv` in the current directory.
