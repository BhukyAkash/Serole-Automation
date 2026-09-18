from datetime import datetime
comp = "Comprehensive"
tpft = "Third Party Fire & Theft"
tpl  = "Third Party Liability"
# pytest -s SAP\test_motor.py::test_pc
# pytest -s SAP\test_motor.py::test_mc

today = datetime.now().strftime("%d.%m.%y")

info = {
    "BP"    : "1000025327",    # "1000025326"    "1000025327"  TFS - Ind-1000024551  Org-1000024653
    "CC"    : "2210000540",    # "2210000540"    "2210001267"   "2210001238"
    "date"  : today, #"15.09.2025",

    "MC" : {
        "pm_id"         : "MTPLMC000000",
        "vehicle_no"    : "VGF3178",
        "coverage_type" : tpl,
        "covpac"        : tpl,
        "si"            : "10000"
    },

    "PC" : {
        "pm_id"         : "MTPLPC000000",
        "vehicle_no"    : "CAPS8H7",
        "si"            : "25000",
        "coverage_type" : tpl,
        "covpac"        : tpl
        }
}

def get_vehicle_info(vehicle_type: str) -> dict:
    if vehicle_type not in info:
        raise KeyError(
            f"Vehicle type '{vehicle_type}' not found. "
            f"Valid types: {list(info.keys())}"
        )
    return info[vehicle_type]
