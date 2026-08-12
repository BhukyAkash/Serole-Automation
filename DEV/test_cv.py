from base_login import incep_date, login, navigation, cv_moto, issue_policy
from excel_utils import get_vehicle_data
from extension import cv_trailer
from base_login import manager_approval
from log_utils import log_dev_policy


def test_cv_motor(page):
    vehicle_data = None
    try:
        print("\n====================== Issuance of CV policy ==================")
        page.wait_for_load_state()
        login(page)
        navigation(page)
        cv_moto(page)

        # ========= FIRST SCREEN ===========

        # ---- VEHICLE REG ----
        vehicle_data = get_vehicle_data("CV")
        page.get_by_role("textbox").first.fill(vehicle_data["vehicle_reg_no"])

        # ---- Place of Use ---
        page.locator(".mat-select-placeholder").click()
        page.get_by_role("option", name="Melaka").click()

        page.get_by_role("button", name="search Vehicle Search").click()
        page.wait_for_timeout(3000)

        # ---- Vehicle Class ----
        page.locator("mat-select#vehClass").click()
        page.get_by_role("option", name="Commercial Vehicle").click()

        # ---- Vehicle Use ----
        page.locator("mat-select#vehUse").click()
        page.get_by_role("option", name="C Permit").click()

        # --- Engine & Chasis No. ----
        page.locator("mat-form-field").filter(has_text="Engine # *").locator("#engineNo").fill("132456")
        page.locator("mat-form-field").filter(has_text="Chassis # *").locator("#chassisNo").fill("987656")

        # ---- Engine Capacity ---
        page.locator('input#cc').fill("1200")

        # ---- MAKE & MODEL ----
        page.locator("mat-select#make").click()
        page.get_by_role("option", name="OPEL").click()

        page.locator("mat-select#model").click()
        page.get_by_role("option", name="FRONTERA").click()

        # ---- Year of Manufacture ----
        page.locator("mat-select#year").click()
        page.get_by_role("option", name="2020").click()
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
        page.get_by_role("option", name="NA").click()

        # ---- Seating Capacity ----
        page.locator("input#seatCapacity").fill("5")
        # ---- Carrying Capacity ----
        page.locator("input#carryingCapacity").fill("10")

        sc = page.locator('input#seatCapacity').input_value().strip()
        cc = page.locator('input#cc').input_value().strip()
        print(f"Engine & Seating Capacity: {cc} || {sc}")

        page.locator("mat-select#loadCarrying").click()
        page.get_by_role("option", name="Tonnes").click()

        # ---- Carriage Goods ----
        page.locator("mat-select#carriageGoods").click()
        page.get_by_role("option", name="Beverages Bottles").click()

        # ---- Save Vehicle Info Button ----
        page.get_by_role("button", name="Save Vehicle Info").click()


        # ========== SECOND SCREEN ==========

        # ---- Coverage Type ----
        page.locator("mat-select#coverageType").click()
        page.get_by_role("option", name="Comprehensive").click()

        selected_coverage = page.locator("#mat-select-value-31").inner_text().strip()
        print("Coverage type: ", selected_coverage)

        # ---- COVERAGE DATE -----
        incep_date(page)

        # ----- SUM INSURED ----
        page.get_by_role("region", name="Coverage").locator("input[type=\"text\"]").click()
        page.get_by_role("region", name="Coverage").locator("input[type=\"text\"]").fill("45000")

        # ---- BUSINESS REGISTRATION NUMBER ----
        page.locator("mat-form-field").filter(has_text="Business Registration # *").locator("#id").fill(vehicle_data["mykad"])

        # ---- NAME AS PER ID / LEGAL NAME ----
        page.locator("dx-input").filter(has_text="* Name as per ID / Legal Name").locator("#legalName").fill("CV C Permit")
        page.get_by_role("button", name="search Validate Owner as per").click()

        # ---- NCD value ----
        page.wait_for_timeout(7000)
        ncd_value = page.locator("#currentNCD input.mat-input-element").input_value()
        print("NCD Value:", ncd_value)

        cv_trailer(page)

        #---- SAVE & NEXT BUTTON -----
        page.get_by_role("button", name="Save & Next").click()
        print("Clicked on Save& Next Button")
        page.wait_for_timeout(10000)


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

        # ---- CHECK IF ADDRESS ALREADY EXISTS ----
        add_button = page.locator("button[name='Add'], button:has-text('Add')").first
        if add_button.is_visible():
            page.wait_for_timeout(5000)
            # scroll button into view
            add_button.scroll_into_view_if_needed()
            page.wait_for_timeout(1000)
            # force click to bypass overlay interception
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
            page.locator("div.box-card").nth(2).click()

        # ---- Declaration Statements ----
        page.get_by_text("We respect your privacy and").click()
        page.get_by_text("I hereby confirm that I have").click()

        # ---- Get Quote Number ----
        quote_text = page.locator("text=Quote Reference #").locator("xpath=following-sibling::*").inner_text()
        quote_number = quote_text.strip()
        print("Quote Number:", quote_number)

        # ====== NSTP FLOW FUNCTION CALL ======
        submit_approval_btn = page.get_by_role("button", name="Submit for TPM Staff Approval")
        if submit_approval_btn.is_visible():
            # ---- Submit for Review Button ----
            submit_approval_btn.click()
            print("Clicked on Submit for TPM Staff Approval button")
            page.wait_for_timeout(30000)

            # ---- Browser launch ---
            browser = page.context.browser
            manager_context = browser.new_context(no_viewport=True)
            manager_page = manager_context.new_page()

            manager_page.goto(f"https://tune.dev.indigit.io/#/qms/quote/motor/rcv/cover-details?edit=true&quoteNr={quote_number}")
            manager_approval(manager_page)
            page.wait_for_timeout(5000)
            page.get_by_role("button", name="Back").click()

        # ==== DEV POLICY ISSUANCE =====
        policy_number = issue_policy(page)

        print("DEV - CV")
        print("Quote Reference:", quote_number)
        print("Policy Number:", policy_number)

        log_dev_policy(
            product="CV",
            quote_number=quote_number,
            policy_number=policy_number,
            coverage_type=selected_coverage,
        )

    finally:
        page.get_by_text("Murali Mohan", exact=True).click()
        page.get_by_text("Sign Out", exact=True).click()
        print("Terminated the session")
        page.wait_for_timeout(4000)