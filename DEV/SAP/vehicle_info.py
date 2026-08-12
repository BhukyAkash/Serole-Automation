info = {
    "BP"    : "1000025326",    # "1000025326"    "1000025327"
    "CC"    : "2210000540",    # "2210000540"    "2210001267"
    "date"  : "01.01.2024",

    "MC" : {
        "pm_id"         : "MTPLMC000000",
        "vehicle_no"    : "VGF3178",
        "coverage_type" : "Comprehensive",     # Third Party
        "covpac"        : "Comprehensive",       
        "si"            : "10000"
    },

    "PC" : {
        "pm_id"         : "MTPLPC000000",
        "vehicle_no"    : "PJC9881",
        "si"            : "25000",
        "coverage_type" : "TP, Fire & Theft",             # "Comprehensive"    "TP, Fire & Theft"
        "covpac"        : "Third Party Fire & Theft",  # "Comprehensive"    "Third Party, Fire and Theft"
        }
}

def get_vehicle_info(vehicle_type: str) -> dict:
    if vehicle_type not in info:
        raise KeyError(
            f"Vehicle type '{vehicle_type}' not found. "
            f"Valid types: {list(info.keys())}"
        )
    return info[vehicle_type]
