import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from base_login import incep_date, issue_policy, login, navigation, pc_moto, motor_prem, quote_letter, policy_letter
from vehicle_info import get_vehicle_info, AUTOMATION_FLAGS, motor_ph_adrs
from utils.excel_utils import get_vehicle_data, pc_excel, mark_policy_issued, reset_on_error
from utils.extension import pc_extension
from utils.nstp_flow import nstp_flow


# ---- Path References ----
BASE_DIR = os.path.join(os.path.dirname(__file__), "..")               # D:\Automation\pages
DOWNLOADS_DIR = os.path.join(os.path.dirname(__file__), "downloads")  # D:\Automation\pages\NB\downloads

# ---- Load PC flags from config ----
flags = AUTOMATION_FLAGS["PC"]

# pytest -s nb\test_pc.py
def test_pc_motor(page):
    vehicle_data = None
    try:
        print("\n====================== Issuance of PC policy ==================")
        username = login(page)
        navigation(page)
        pc_moto(page)

        # ---- Load PC vehicle info ----
        vehicle_info = get_vehicle_info("PC")

        # ========= FIRST SCREEN ===========

        # ---- VEHICLE REG ----
        vehicle_data = get_vehicle_data("PC")
        if vehicle_data is None:
            return

        print(f"Vehicle Regio: {vehicle_data["vehicle_reg_no"]}")
        print(f"MY KadID: {vehicle_data["mykad"]}")

        # ---- BP & NCDRequestV2 Service Logs  ----
        page.net_logger.set_vehicle_reg(vehicle_data["vehicle_reg_no"])

        # ----- Input of Vehicle Regio -------
        page.wait_for_load_state("networkidle")
        page.get_by_role("textbox").first.fill(vehicle_data["vehicle_reg_no"])

        # ---- Place of Use ----
        page.locator(".mat-select-placeholder").click()
        page.get_by_role("option", name=vehicle_info["place_of_use"]).click()

        # ---- Vehicle Search ----
        page.get_by_role("button", name="search Vehicle Search").click()
        page.wait_for_timeout(5000)

        # ------- Active Policy Exists -------
        try:
            renewal_popup = page.locator("mat-dialog-content",has_text="Insurance can be only renewed within 60 days prior to expiry.")
            if renewal_popup.is_visible(timeout=3000):
                print("Renewal popup displayed")
                page.locator("span.popup-close").click()
                mark_policy_issued(vehicle_data["vehicle_type"], vehicle_data["claimed_row"])
                return
        except Exception:
            pass

        try:
            page.get_by_role("menuitem", name="edit").click(timeout=2000)
            page.get_by_role("button", name="Proceed").click()
            page.wait_for_timeout(2000)
        except:
            pass

        # ---- MAKE / MODEL / YEAR ----
        if vehicle_info["change_vehicle"]:
            make_dropdown = page.locator("mat-select#make")
            if make_dropdown.is_visible():
                make_dropdown.click()
                page.get_by_role("option", name=vehicle_info["make"]).click()
                page.wait_for_timeout(1000)
            else:
                print("Make dropdown not visible, skipping")

            model_dropdown = page.locator("mat-select#model")
            if model_dropdown.is_visible():
                model_dropdown.click()
                page.get_by_role("option", name=vehicle_info["model"]).click()
                page.wait_for_timeout(1000)
            else:
                print("Model dropdown not visible, skipping")

            # ---- VARIANT ----
            variant = page.locator("mat-select#variant")
            if variant.is_visible():
                variant.click()
                page.get_by_role("option", name=vehicle_info["variant"]).click()
                page.wait_for_timeout(1000)
            else:
                print("Variant not visible, skipping")

        else:
            pass

        if vehicle_info["year_of_manufacture"]:
            year_dropdown = page.locator("mat-select#year")
            if year_dropdown.is_visible():
                year_dropdown.click()
                page.get_by_role("option", name=vehicle_info["year"]).click()
            else:
                print("Year dropdown not visible, skipping")
        else:
            pass

        # ---- READ BACK FOR LOGGING ----
        make  = page.locator("#make .mat-select-min-line").inner_text()
        model = page.locator("#model .mat-select-min-line").inner_text()
        year  = page.locator("#year .mat-select-min-line").inner_text()
        print(f"Make: {make} | Model: {model} | Year: {year}")

        # --- Engine Capacity field ----
        cc_input = page.locator('input#cc')
        if cc_input.is_visible():
            current_value = cc_input.input_value().strip()
            if current_value == "" or current_value == "0":
                cc_input.dblclick()
                cc_input.fill(vehicle_info["engine_capacity"])
            else:
                pass

        # --- Seating Capacity field ----
        seat_input = page.locator('input#seatCapacity')
        if seat_input.is_visible():
            current_value = seat_input.input_value().strip()
            if current_value == "" or current_value == "0":
                seat_input.dblclick()
                seat_input.fill(vehicle_info["seating_capacity"])
            else:
                pass

        sc = page.locator('input#seatCapacity').input_value().strip()
        cc = page.locator('input#cc').input_value().strip()
        print(f"Engine & Seating Capacity: {cc} || {sc}")

        # ---- Vehicle Age (for logging only) ----
        vehicle_age_locator = page.locator("mat-form-field").filter(has_text="Vehicle Age").locator("#vehicleAge")
        vehicle_age_text = vehicle_age_locator.input_value().strip()

        vehicle_age = int(vehicle_age_text)
        print(f"Vehicle Age: {vehicle_age} years")

        # ---- SAVE VEHICLE DETAILS  ----
        search_vehicle = page.get_by_role("button", name="Save Vehicle Info").first
        try:
            search_vehicle.wait_for(state="visible", timeout=5000)
            search_vehicle.click()
            page.wait_for_load_state("networkidle")
        except:
            print("Save Vehicle Info button not available")


        # ========== SECOND SCREEN ==========

        # ---- COVERAGE TYPE (read default) ----
        selected_coverage = page.locator("#mat-select-value-9 span.mat-select-min-line").inner_text().strip()
        print("Default Coverage type: ", selected_coverage)

        # ---- COVERAGE TYPE ----
        if vehicle_info["change_coverage"]:
            page.locator("#mat-select-value-9").click()
            page.get_by_role("option", name=vehicle_info["coverage_type"]).click()
            print(f"Coverage type changed to: {vehicle_info['coverage_type']}")
        else:
            pass

        selected_coverage = page.locator("#mat-select-value-9").inner_text().strip()
        print("Selected Coverage type: ", selected_coverage)

        # ---- COVERAGE DATE -----
        incep_date(page)

        # ---- MARKET VALUE ----
        market_value_text = page.locator("mat-form-field").filter(has_text="Market Value").locator("#ismMarketValue").input_value().strip()
        market_value = int(float(market_value_text.replace(",", "")))
        print(f"Market Value: {market_value}")

        # ---- VEHICLE SUM INSURED ----
        page.wait_for_timeout(1000)
        if "Third Party" not in selected_coverage:
            page.wait_for_timeout(2000)
            sum_insured = str(market_value) if market_value > 5000 else "5000"
            print(f"Sum Insured: {sum_insured}")

            page.locator("dx-input-currency").filter(has_text="* Vehicle Sum Insured *").locator("#sumInsured").click()
            page.locator("dx-input-currency").filter(has_text="* Vehicle Sum Insured *").locator("#sumInsured").fill(sum_insured)
        else:
            print("Third Party coverage selected")

        #---- MYKAD ID ----
        page.locator("mat-form-field").filter(has_text="ID # * help").locator("#id").fill(vehicle_data["mykad"])

        #----NAME OF THE PH ----
        page.locator("mat-form-field").filter(has_text="Name as per ID *").locator("#legalName").fill("PC")
        page.get_by_role("button", name="search Validate Owner as per").click()

        # ==== Multi Contract / Extensions ====
        print("======== Extension Coverage Selection ========")

        if flags["explore_extensions"]:
            pc_extension(page, selected_coverage, flags)
        else:
            print("No Extensions Selected")

        # ---- NCD value ----
        page.wait_for_timeout(7000)
        ncd_value = page.locator("#currentNCD input.mat-input-element").input_value()
        print("NCD Value:", ncd_value)

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


        # ========== THIRD SCREEN === COVER DETAILS ==========

        # ---- DRIVER EXPERIENCE ----
        page.locator(".mat-select-placeholder").first.click()
        page.get_by_role("option", name="Less than 2 years").click()

        # ----- Premiums -----
        sum_insured, act_prem, basic_prem, ncd, after_ncd, gross_premium, sst, stamp_duty, total = motor_prem(page)

        # ---- CHECK IF YES BUTTON EXISTS AND IS ENABLED ----
        yes_button = page.get_by_role("button", name="Yes").first

        if yes_button.is_visible():
                yes_button.click()
                page.wait_for_timeout(1000)

        # ---- Policyholder Residential Adress ---
        motor_ph_adrs(page)

        # ---- Garage Types ----
        page.locator(".mat-select-placeholder").first.click()
        page.get_by_role("option", name="Public Road").click()
        page.locator(".mat-select-placeholder").first.click()
        page.get_by_role("option", name="No Alarm(WITHOUT MECHANICAL").click()
        page.locator(".mat-select-placeholder").click()
        page.get_by_role("option", name="ABS(No Airbags)").click()

        # ---- Declaration Statements ----
        page.locator("label").filter(has_text="We respect your privacy").click()
        page.get_by_text("I hereby confirm that I have").click()

        # ---- Policy Holder Name ----
        ph_name = page.locator(".qms-canvas-card-title-wrapper .heading-6").first.inner_text().strip()
        print("Policy Holder name: ", ph_name)

        # ---- Get Quote Number -----
        quote_text = page.locator("text=Quote Reference #").locator("xpath=following-sibling::*").inner_text()
        quote_number = quote_text.strip()
        print("Quote Number:", quote_number)

        # ---- Create Quotenr_vl ----
        page.net_logger.set_quote_number(quote_number)

        # ====== NSTP FLOW FUNCTION CALL ======
        generate_quote_btn = nstp_flow(page, quote_number, vehicle_type="pc")

        # ---- Generate Quote Flow ----
        # quote_letter(page)

        # ==== Issue Policy function ====
        policy_number = issue_policy(page)
        mark_policy_issued(vehicle_data["vehicle_type"], vehicle_data["claimed_row"])

        # ---- Download the policy schedule ----
        # policy_letter(page)

        # --- Issue Policy Service call ----
        page.net_logger.set_policy_number(policy_number)

        # --------- SAVE TO EXCEL ---------
        pc_excel(selected_coverage, quote_number, policy_number,
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