import pytest
from base_login import incep_date, login, navigation, pc_moto, issue_policy, nstp_flow
from excel_utils import get_vehicle_data, mark_policy_issued, reset_on_error
from extension import pc_extension, AUTOMATION_FLAGS
from log_utils import log_dev_policy

def test_pc_motor(page):

    claimed_row = None

    try:
        print("\n====================== Issuance of DEV - PC policy ==================")
        login(page)
        navigation(page)
        pc_moto(page)

        # ========= FIRST SCREEN ===========
        
        # ---- VEHICLE REG ----
        vehicle_data = get_vehicle_data("PC")
        if vehicle_data is None:
            pytest.skip("No available PC test data (all rows Y/RUNNING)")

        claimed_row = vehicle_data["claimed_row"]
        page.get_by_role("textbox").first.fill(vehicle_data["vehicle_reg_no"])

        # ---- Place of Use ----
        page.locator(".mat-select-placeholder").click()
        page.get_by_role("option", name="Melaka").click()

        # ---- Vehicle Search ----
        page.get_by_role("button", name="search Vehicle Search").click()
        page.wait_for_timeout(5000)

        # ------- Active Policy Exists -------
        try:
            renewal_popup = page.locator("mat-dialog-content",has_text="Insurance can be only renewed within 60 days prior to expiry.")
            if renewal_popup.is_visible(timeout=3000):
                print("Renewal popup displayed")
                page.locator("span.popup-close").click()
                mark_policy_issued("PC", claimed_row)
                return
        except Exception:
            pass

        try:
            page.get_by_role("menuitem", name="edit").click(timeout=3000)
            page.get_by_role("button", name="Proceed").click()
            page.wait_for_timeout(2000)
        except:
            pass

        # --- Engine Capacity field ----
        cc_input = page.locator('input#cc')
        if cc_input.is_visible():
            current_value = cc_input.input_value().strip()
            if current_value == "" or current_value == "0":
                cc_input.dblclick()
                cc_input.fill("1200")
            else:
                print(f"Engine Capacity: {current_value}")

        # --- Seating Capacity field ----
        seat_input = page.locator('input#seatCapacity')

        if seat_input.is_visible():
            current_value = seat_input.input_value().strip()
            if current_value == "" or current_value == "0":
                seat_input.dblclick()
                seat_input.fill("2")
            else:
                print(f"Seating Capacity: {current_value}")
        
        # ---- Vehicle Age (to determine coverage type) ---- 
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
        # page.locator("#mat-select-value-9").click()
        # page.get_by_role("option", name="Comprehensive").click()

        # --- Condition for coverage if needed ----
        page.locator("#mat-select-value-9").click()
        if vehicle_age >= 20:
            page.get_by_role("option", name="Third Party Fire & Theft").click()
        else:
            page.get_by_role("option", name="Comprehensive").click()

        selected_coverage = page.locator("#mat-select-value-9").inner_text().strip()
        print("Selected Coverage type: ", selected_coverage)

        # ---- COVERAGE DATE -----
        incep_date(page)

        # ---- MARKET VALUE ----
        market_value_text = page.locator("mat-form-field").filter(has_text="Market Value").locator("#ismMarketValue").input_value().strip()
        market_value = int(float(market_value_text.replace(",", "")))
        print(f"Market Value: {market_value}")

        # ---- VEHICLE SUM INSURED ----
        sum_insured = str(market_value) if market_value > 5000 else "5000"
        print(f"Sum Insured: {sum_insured}")

        page.locator("dx-input-currency").filter(has_text="* Vehicle Sum Insured *").locator("#sumInsured").click()
        page.locator("dx-input-currency").filter(has_text="* Vehicle Sum Insured *").locator("#sumInsured").fill(sum_insured)

        #---- MYKAD ID ----
        page.locator("mat-form-field").filter(has_text="ID # * help").locator("#id").fill(vehicle_data["mykad"])

        #----NAME OF THE PH ----
        page.locator("mat-form-field").filter(has_text="Name as per ID *").locator("#legalName").fill("PC")
        page.get_by_role("button", name="search Validate Owner as per").click()

        # ==== Multi Contract / Extensions ====
        if AUTOMATION_FLAGS["PC"]["explore_extensions"]:
            pc_extension(page, selected_coverage)
            print("Extensions Amended")
        else:
            print("Extension Coverage skipped")

        # ---- NCD value ----
        page.wait_for_timeout(4000)
        ncd_value = page.locator("#currentNCD input.mat-input-element").input_value()
        print("NCD Value:", ncd_value, "%")

        #---- SAVE & NEXT BUTTON -----
        page.get_by_role("button", name="Save & Next").click()
        print("Clicked on Save& Next Button")
        page.wait_for_timeout(10000)


        # ========== THIRD SCREEN === COVER DETAILS ==========

        # ---- DRIVER EXPERIENCE ----
        page.locator(".mat-select-placeholder").first.click()
        page.get_by_role("option", name="Less than 2 years").click()

        # ---- CHECK IF YES BUTTON EXISTS AND IS ENABLED ----
        yes_button = page.get_by_role("button", name="Yes").first

        if yes_button.is_visible():
            yes_button.click()
            page.wait_for_timeout(7000)

        # ---- CHECK IF ADDRESS ALREADY EXISTS ----
        add_button = page.locator("button[name='Add'], button:has-text('Add')").first
        if add_button.is_visible():
            page.wait_for_timeout(5000)
            add_button.scroll_into_view_if_needed()
            page.wait_for_timeout(1000)
            add_button.click(force=True)

            print("Clicked on Add button")

        # ---- STATE ---- (runs for both cases)
        page.locator(".mat-select-placeholder").first.click()
        page.get_by_role("option", name="Johor").click()
        page.wait_for_timeout(3000)

        # ---- PINCODE ----
        page.locator(".mat-select-placeholder").first.click()
        page.get_by_role("option", name="81100").click()
        page.wait_for_timeout(2000)

        # ---- STREET ADDRESS ----
        page.get_by_role("combobox", name="Address Line").first.click()
        page.get_by_role("option", name="Taman Desa Harmoni", exact=True).click()
        page.wait_for_timeout(2000)

        # ---- SAVE BUTTON (if address is added) ----
        address_save = page.locator("button#save")
        if address_save.is_visible():
            address_save.click()
            page.locator("div.box-card").nth(1).click()
        
        # ---- Garage Types ----
        page.locator(".mat-select-placeholder").first.click()
        page.get_by_role("option", name="Public Road").click()
        page.locator(".mat-select-placeholder").first.click()
        page.get_by_role("option", name="No Alarm(WITHOUT MECHANICAL").click()
        page.locator(".mat-select-placeholder").click()
        page.get_by_role("option", name="ABS(No Airbags)").click()

        # ---- Declaration Statements ----
        page.get_by_text("We respect your privacy and").click()
        page.get_by_text("I hereby confirm that I have").click()

        # ---- Get Quote Number -----
        quote_text = page.locator("text=Quote Reference #").locator("xpath=following-sibling::*").inner_text()
        quote_number = quote_text.strip()
        print("Quote Number:", quote_number)

        # ==== NSTP FLOW ===
        nstp_flow(page, quote_number, vehicle_type="pc")

        # ==== DEV POLICY ISSUANCE =====
        policy_number = issue_policy(page)

        print("DEV - PC")
        print("Quote Reference:", quote_number)
        print("Policy Number:", policy_number)

        log_dev_policy(
            product="PC",
            quote_number=quote_number,
            policy_number=policy_number,
            coverage_type=selected_coverage,
        )

        mark_policy_issued("PC", claimed_row)

    except Exception:
        if claimed_row is not None:
            reset_on_error("PC", claimed_row)
        raise

    finally:
        page.get_by_text("Murali Mohan", exact=True).click()
        page.get_by_text("Sign Out", exact=True).click()