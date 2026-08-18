import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from base_login import incep_date, issue_policy, login, navigation, cv_moto, motor_prem, quote_letter, policy_letter
from utils.excel_utils import get_vehicle_data, cv_excel, mark_policy_issued, reset_on_error
from vehicle_info import get_vehicle_info, AUTOMATION_FLAGS, motor_business_adrs
from utils.extension import cv_extension
from utils.nstp_flow import nstp_flow
from utils.test_mail import send_email

# ---- Path References ----
BASE_DIR = os.path.join(os.path.dirname(__file__), "..")               # D:\Automation\pages
DOWNLOADS_DIR = os.path.join(os.path.dirname(__file__), "downloads")  # D:\Automation\pages\NB\downloads

# ---- Load PC flags from config ----
flags = AUTOMATION_FLAGS["CV"]

# pytest -s nb\test_cv.py
def test_cv_motor(page):
    vehicle_data = None
    try:
        print("\n====================== Issuance of CV policy ==================")
        page.wait_for_load_state()
        username = login(page)
        navigation(page)
        cv_moto(page)

        # ---- Load vehicle info ----
        vehicle_info = get_vehicle_info("CV")

        # ========= FIRST SCREEN ===========

        # ---- VEHICLE REG ----
        vehicle_data = get_vehicle_data("CV")
        if vehicle_data is None:
            return

        print(f"Vehicle Regio: {vehicle_data["vehicle_reg_no"]}")
        print(f"MY KadID: {vehicle_data["mykad"]}")

        # ---- START NETWORK LOGGING (bp, ncdRequestV2, quote) ----
        page.net_logger.set_vehicle_reg(vehicle_data["vehicle_reg_no"])

        page.get_by_role("textbox").first.fill(vehicle_data["vehicle_reg_no"])

        # ---- Place of Use ---
        page.locator(".mat-select-placeholder").click()
        page.get_by_role("option", name=vehicle_info["place_of_use"]).click()

        page.get_by_role("button", name="search Vehicle Search").click()
        page.wait_for_timeout(3000)

        # ---- Vehicle Class ----
        page.locator("mat-select#vehClass").click()
        page.get_by_role("option", name=vehicle_info["vehicle_class"]).click()

        # ---- Vehicle Use ----
        page.locator("mat-select#vehUse").click()
        page.get_by_role("option", name=vehicle_info["vehicle_use"]).click()

        # --- Engine & Chasis No. ----
        page.locator("mat-form-field").filter(has_text="Engine # *").locator("#engineNo").fill(vehicle_info["engine_no"])
        page.locator("mat-form-field").filter(has_text="Chassis # *").locator("#chassisNo").fill(vehicle_info["chassis_no"])

        # ---- Engine Capacity ---
        page.locator('input#cc').fill(vehicle_info["engine_capacity"])

        # ---- MAKE & MODEL ----
        page.locator("mat-select#make").click()
        page.get_by_role("option", name=vehicle_info["make"]).click()

        page.locator("mat-select#model").click()
        page.get_by_role("option", name=vehicle_info["model"]).click()

        # ---- Year of Manufacture ----
        page.locator("mat-select#year").click()
        page.get_by_role("option", name=vehicle_info["year"]).click()
        page.wait_for_timeout(2000)

        # ---- READ BACK FOR LOGGING ----
        make = page.locator("#make .mat-select-min-line").inner_text()
        model = page.locator("#model .mat-select-min-line").inner_text()
        year = page.locator("#year .mat-select-min-line").inner_text()
        print(f"Make: {make} | Model: {model} | Year: {year}")

        # ---- Vehicle Age (to determine coverage type) ----
        vehicle_age_text = page.locator("input#vehicleAge").input_value().strip()
        vehicle_age = int(vehicle_age_text)
        print(f"Vehicle Age: {vehicle_age} years")

        # ---- VARIANT ----
        page.locator("mat-select#variant").click()
        page.get_by_role("option", name=vehicle_info["variant"]).click()

        # ---- Seating Capacity ----
        page.locator("input#seatCapacity").fill(vehicle_info["seating_capacity"])
        # ---- Carrying Capacity ----
        page.locator("input#carryingCapacity").fill(vehicle_info["carrying_capacity"])

        sc = page.locator('input#seatCapacity').input_value().strip()
        cc = page.locator('input#cc').input_value().strip()
        print(f"Engine & Seating Capacity: {cc} || {sc}")

        page.locator("mat-select#loadCarrying").click()
        page.get_by_role("option", name=vehicle_info["carrying_capacity_unit"]).click()

        # ---- Carriage Goods ----
        page.locator("mat-select#carriageGoods").click()
        page.get_by_role("option", name=vehicle_info["carriage_goods"]).click()

        # ---- Save Vehicle Info Button ----
        page.get_by_role("button", name="Save Vehicle Info").click()


        # ========== SECOND SCREEN ==========

        # ---- Coverage Type ----
        page.locator("mat-select#coverageType").click()
        if vehicle_info["change_coverage"]:
            page.get_by_role("option", name=vehicle_info["coverage_type"]).click()
        else:
            if vehicle_age >= 20:
                page.get_by_role("option", name="TP, Fire & Theft").click()
            else:
                page.get_by_role("option", name="Comprehensive").click()

        selected_coverage = page.locator("#mat-select-value-31").inner_text().strip()
        print("Selected Coverage type: ", selected_coverage)

        # ---- COVERAGE DATE -----
        incep_date(page)

        # ----- SUM INSURED ----
        page.get_by_role("region", name="Coverage").locator("input[type=\"text\"]").click()
        page.get_by_role("region", name="Coverage").locator("input[type=\"text\"]").fill(vehicle_info["sum_insured"])

        # ---- BUSINESS REGISTRATION NUMBER ----
        page.locator("mat-form-field").filter(has_text="Business Registration # *").locator("#id").fill(vehicle_data["mykad"])

        # ---- NAME AS PER ID / LEGAL NAME ----
        page.locator("dx-input").filter(has_text="* Name as per ID / Legal Name").locator("#legalName").fill("CV C Permit")
        page.get_by_role("button", name="search Validate Owner as per").click()

        # ---- NCD value ----
        page.wait_for_timeout(7000)
        ncd_value = page.locator("#currentNCD input.mat-input-element").input_value()
        print("NCD Value:", ncd_value)

        # ==== Multi Contract / Extensions ====
        print("======== Extension Coverage Selection ========")

        if flags["explore_extensions"]:
            cv_extension(page, selected_coverage, flags)
        else:
            print("No Extensions Selected")
        
        #---- SAVE & NEXT BUTTON -----
        try:
            page.get_by_role("button", name="Save & Next").click()
        except Exception as e:
            if "TimeoutError" in type(e).__name__ or "Timeout" in str(e):
                print("Vehicle data already used in system, stopping the execution.")
                mark_policy_issued(vehicle_data["vehicle_type"], vehicle_data["claimed_row"])
                return
            raise
        print("Registration Number is Triggered to ISM")
        page.wait_for_timeout(5000)
        
        # ========== THIRD SCREEN ==== PH Details ======
        
        # ---- CHECK IF YES BUTTON EXISTS AND IS ENABLED ----
        try:
            yes_button = page.get_by_role("button", name="Yes").first
            yes_button.wait_for(state="visible", timeout=12000)
            yes_button.click()
            page.wait_for_timeout(1000)
            print("Yes button clicked")
        except:
            print("Yes button not visible, skipping")

        # ----- Premiums -----
        sum_insured, act_prem, basic_prem, ncd, after_ncd, gross_premium, sst, stamp_duty, total = motor_prem(page)

        # ---- Policyholder Residential Adress ---
        motor_business_adrs(page)

        # ---- Declaration Statements ----
        page.locator("label").filter(has_text="We respect your privacy").click()
        page.get_by_text("I hereby confirm that I have").click()

        # ---- Get Quote Number ----
        quote_text = page.locator("text=Quote Reference #").locator("xpath=following-sibling::*").inner_text()
        quote_number = quote_text.strip()
        print("Quote Number:", quote_number)

        # ---- Create Quotenr_vl ----
        page.net_logger.set_quote_number(quote_number)

        # ====== NSTP FLOW FUNCTION CALL ======
        nstp_flow(page, quote_number, vehicle_type="cv")

        # ---- Generate Quote Flow ----
        # quote_letter(page)

        # ==== Issue Policy function ====
        policy_number = issue_policy(page)
        mark_policy_issued(vehicle_data["vehicle_type"], vehicle_data["claimed_row"])

        # ---- Download the policy schedule ----
        #policy_letter(page)

        # --- Issue Policy Service call ----
        page.net_logger.set_policy_number(policy_number)

        
        # --------- SAVE TO EXCEL ---------
        cv_excel(selected_coverage, quote_number, policy_number,
        sum_insured, act_prem, basic_prem, ncd,
        after_ncd, gross_premium, sst, stamp_duty, total)


        # -------- SEND EMAIL ---------
        # try:
        #     send_email()
        # except Exception as e:
        #     print("Email failed:", e)


    except Exception as e:
        print(f"Test failed: {e}")
        if vehicle_data:
            reset_on_error(vehicle_data["vehicle_type"], vehicle_data["claimed_row"])
        raise

    finally:
        page.get_by_text(username, exact=True).click()
        page.get_by_text("Sign Out", exact=True).click()
        print("Terminated the session")
        page.wait_for_timeout(4000)