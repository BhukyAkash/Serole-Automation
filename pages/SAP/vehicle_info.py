import os
from datetime import datetime
from openpyxl import load_workbook

excel_path = os.path.join(os.path.dirname(__file__), "BP Test Data.xlsx")
wb = load_workbook(excel_path)

sheet_pc = wb["PC"]
sheet_mc = wb["MC"]

# pytest -s SAP\test_motor.py::test_pc
# pytest -s SAP\test_motor.py::test_mc
# --- PC Test Data ----
cell_pc = 22
# --- MC Test Data ---- 
cell_mc = 10

comp = "Comprehensive"
tpft = "Third Party Fire & Theft"
tpl = "Third Party Liability"

today = datetime.now().strftime("%d.%m.%y")

info = {
    "BP_PC" : sheet_pc.cell(row=cell_pc, column=3).value,
    "BP_MC" : sheet_mc.cell(row=cell_mc, column=3).value,
    "CC"    : "2210001629",
    "date"  : today,        #"01.04.2024"

    "MC" : {
        "pm_id"         : "MTPLMC000000",
        "vehicle_no"    : sheet_mc.cell(row=cell_mc, column=1).value,
        "coverage_type" : comp,
        "covpac"        : comp,
        "si"            : "10000"
    },

    "PC" : {
        "pm_id"         : "MTPLPC000000",
        "vehicle_no"    : sheet_pc.cell(row=cell_pc, column=1).value,
        "si"            : "25000",  
        "coverage_type" : tpft,
        "covpac"        : tpft,
        }
}


def get_vehicle_info(vehicle_type: str) -> dict:
    if vehicle_type not in info:
        raise KeyError(
            f"Vehicle type '{vehicle_type}' not found. "
            f"Valid types: {list(info.keys())}"
        )
    return info[vehicle_type]
