import os
from datetime import datetime

LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "RunLogs")
os.makedirs(LOG_DIR, exist_ok=True)

DEV_MASTER_LOG = os.path.join(LOG_DIR, "DEV_Master_Policies.log")


def _ensure_master_header():
    """Write the master banner once, only if the file is new/empty."""
    if not os.path.exists(DEV_MASTER_LOG) or os.path.getsize(DEV_MASTER_LOG) == 0:
        with open(DEV_MASTER_LOG, "w", encoding="utf-8") as f:
            f.write("=" * 60 + "\n")
            f.write("  TIPS DEV — Master Policy Issuance Log (All Products)\n")
            f.write("=" * 60 + "\n\n")


def log_dev_policy(product, quote_number, policy_number, env="DEV", **extra_fields):
    """
    Append a DEV-environment policy issuance entry to the single
    consolidated DEV master log. Non-DEV entries (SIT, UAT, etc.)
    are silently skipped so this file stays DEV-only.

    extra_fields = any product-specific details you want printed,
    e.g. coverage_type="Comprehensive", mykad="...", occupation_class="..."
    """
    if env.upper() != "DEV":
        return

    _ensure_master_header()
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    label_map = {
        "coverage_type": "Coverage Type",
        "mykad": "MY KAD ID",
        "policy_title": "Policy Title",
        "occupation_class": "Occupation Class",
    }

    with open(DEV_MASTER_LOG, "a", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write(f"  TIPS DEV — {product} Policy Issuance Log\n")
        f.write("=" * 60 + "\n")
        f.write(f"  Timestamp        : {timestamp}\n")
        f.write(f"  Product          : {product}\n")
        f.write(f"  Quote Number     : {quote_number}\n")
        f.write(f"  Policy Number    : {policy_number}\n")
        for key, value in extra_fields.items():
            label = label_map.get(key, key.replace("_", " ").title())
            f.write(f"  {label:<17}: {value}\n")
        f.write("=" * 60 + "\n\n")