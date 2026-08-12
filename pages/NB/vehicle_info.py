VEHICLE_INFO = {
    "PC": {
        # ---- Vehicle Search ----
        "place_of_use": "Johor",

        # ---- Make / Model / Year ----
        "change_vehicle": False,
        "make": "HONDA",
        "model": "HR-V",
        "variant" : "NA",

        "year_of_manufacture": False,
        "year": "2021",

        # ---- Capacities ----
        "engine_capacity": "1200",
        "seating_capacity": "2",

        # ---- Coverage ----
        "change_coverage": False,
        "coverage_type": "Comprehensive",  # "Comprehensive" or "TP, Fire & Theft" "Third Party"

    },
    "MC": {
        # ---- Vehicle Search ----
        "place_of_use": "Melaka",

        # ---- Make / Model / Year ----
        "change_vehicle": False,
        "make": "HONDA",
        "model": "SL",

        "year_of_manufacture": True,
        "year": "2020",

        # ---- Capacities ----
        "engine_capacity": "125",
        "seating_capacity": "2",

        # ---- Coverage ----
        "change_coverage": True,
        "coverage_type": "Comprehensive",  # "Comprehensive" or "Third Party"

    },
    "CV": {
        # ---- Vehicle Search ----
        "place_of_use": "Kelantan",

        # ---- Vehicle Class / Use ----
        "vehicle_class": "Commercial Vehicle",
        "vehicle_use": "C permit",

        # ---- Engine / Chassis ----
        "engine_no": "63547",
        "chassis_no": "34576657",

        # ---- Make / Model / Year ----
        "make": "PERODUA",
        "model": "RUSA",
        "year": "2021",
        "variant": "NA",

        # ---- Capacities ----
        "engine_capacity": "1200",
        "seating_capacity": "2",
        "carrying_capacity": "1",
        "carrying_capacity_unit": "Tonnes",  # "Tonnes" or "Kg"

        # ---- Carriage Goods ----
        "carriage_goods": "Beverages Bottles",

        # ---- Coverage ----
        "change_coverage": True,
        "coverage_type": "TP, Fire & Theft",  # "Comprehensive" or "TP, Fire & Theft"

        # --- Sum Insured ---
        "sum_insured": "10000",
    }
}

def get_vehicle_info(vehicle_type: str) -> dict:
    if vehicle_type not in VEHICLE_INFO:
        raise KeyError(
            f"Vehicle type '{vehicle_type}' not found. "
            f"Valid types: {list(VEHICLE_INFO.keys())}"
        )
    return VEHICLE_INFO[vehicle_type]

AUTOMATION_FLAGS = {

    "MC": {
        "explore_extensions":   True,   # Click on Extension Coverage button?
        "select_autobuddy"  :   False,   # Select Motorcyclist PA Contract?
        "select_extensions" :   False,   # Select individual extensions?
    },

    "PC": {
        "explore_extensions":   True,   # Click on Extension Coverage button?
        "select_autobuddy":     False,  # Select Autobuddy package?
        "select_extensions":    False,   # Select individual extensions?
    },

    "CV": {
        "explore_extensions":   True,  # Click on Extension Coverage button?
        "select_autobuddy":     False,  # Select Motorist PA package?
        "select_extensions":    False,  # Select individual extensions?
    },
}

ADRESS = {
    # ---- Policy Holder Address ----
    "state": "Perlis",
    "pin"  : "01500",
    "adrs" : "DYMM Tuanku Raja Perlis"
}

def motor_ph_adrs(page):
        # ---- Proposer Residential Address section ---
        section = page.locator("div.mt-3", has_text="Policyholder Residential Address")

        # Second div = address cards, Third div = error message
        address_cards = section.locator("app-address-details, app-address-details-card")
        error_locator = section.locator(".error-color", has_text="Please provide the complete address information")

        address_count = address_cards.count()
        print("Address Count: ", address_count)

        address_selected = False

        for i in range(address_count):
            card = address_cards.nth(i)
            card.locator("label").click()
            page.wait_for_timeout(500)  # allow error div to update after selection

            has_error = error_locator.count() > 0
            print(f"Address {i+1} selected -> Error showing: {has_error}")

            if not has_error:
                print(f"Address {i+1} is complete and selected. Stopping.")
                address_selected = True
                break

        if not address_selected:
            # ---- None of the existing addresses are complete -> Add new one ----
            print("No complete address found. Adding new address.")
            add_button = section.get_by_role("button", name="Add")

            if add_button.count() > 0:
                add_button.click()
                page.wait_for_timeout(1000)
            else:
                print("No 'Add' button found — capturing screenshot for inspection.")

            # ---- STATE ----
            page.locator(".mat-select-placeholder").first.click()
            page.get_by_role("option", name=ADRESS["state"]).click()

            # ---- PINCODE ----
            page.locator(".mat-select-placeholder").first.click()
            page.get_by_role("option", name=ADRESS["pin"]).click()

            # ---- STREET ADDRESS ----
            page.get_by_role("combobox", name="Address Line").first.click()
            page.get_by_role("option", name=ADRESS["adrs"], exact=True).click()

            # ---- SAVE BUTTON ----
            address_save = page.locator("button#save")
            if address_save.is_visible():
                address_save.wait_for(state="visible", timeout=5000)
                address_save.click()

def motor_business_adrs(page):
    # ---- Business Address section ----
    section = page.locator("div.mt-3", has_text="Business Address")

    # Second div = address cards, Third div = error message
    address_cards = section.locator("app-address-details, app-address-details-card")
    error_locator = section.locator(".error-color", has_text="Please provide the complete address information")

    address_count = address_cards.count()
    print("Address Count: ", address_count)

    address_selected = False

    for i in range(address_count):
        card = address_cards.nth(i)
        card.locator("label").click()
        page.wait_for_timeout(500)  # allow error div to update after selection

        has_error = error_locator.count() > 0
        print(f"Address {i+1} selected -> Error showing: {has_error}")

        if not has_error:
            print(f"Address {i+1} is complete and selected. Stopping.")
            address_selected = True
            break

    if not address_selected:
        # ---- None of the existing addresses are complete -> Add new one ----
        print("No complete address found. Adding new address.")
        add_button = section.get_by_role("button", name="Add")

        if add_button.count() > 0:
            add_button.click()
            page.wait_for_timeout(1000)
        else:
            print("No 'Add' button found — capturing screenshot for inspection.")

        # ---- STATE ----
        page.locator(".mat-select-placeholder").first.click()
        page.get_by_role("option", name=ADRESS["state"]).click()

        # ---- PINCODE ----
        page.locator(".mat-select-placeholder").first.click()
        page.get_by_role("option", name=ADRESS["pin"]).click()

        # ---- STREET ADDRESS ----
        page.get_by_role("combobox", name="Address Line").first.click()
        page.get_by_role("option", name=ADRESS["adrs"], exact=True).click()

        # ---- SAVE BUTTON ----
        address_save = page.locator("button#save")
        if address_save.is_visible():
            address_save.wait_for(state="visible", timeout=5000)
            address_save.click()

def pa_ph_adrs(page):
    # ---- Proposer Residential Address section ---
    section = page.locator("div.mt-3", has_text="Proposer Residential Address")
    print("Matched section count:", section.count())
    print("Add button count inside section:", section.get_by_role("button", name="Add").count())

    # --- Address Count of Policy Holder ----- 
    address_cards = section.locator("app-address-details-card")
    address_count = address_cards.count()
    print("Address Count: ", address_count)

    for i in range(address_count):
        card = address_cards.nth(i)
        text = card.locator(".subbody").inner_text().strip()
        print(f"Address {i+1}: '{text}'")

    # Error is section-level, not per-card
    error_locator = section.locator(".error-color", has_text="Please provide the complete address information")
    has_error = error_locator.count() > 0
    print(f"Section has error: {has_error}")

    # ---- If no address present, OR existing address is incomplete, fill new address ----
    if address_count == 0 or has_error:
        add_button = section.get_by_role("button", name="Add")

        if add_button.count() > 0:
            add_button.click()
            page.wait_for_timeout(1000)
        else:
            print("No 'Add' button found")

        # ---- STATE ----
        page.locator(".mat-select-placeholder").first.click()
        page.get_by_role("option", name=ADRESS["state"]).click()
        page.wait_for_timeout(1000)

        # ---- PINCODE ----
        page.locator(".mat-select-placeholder").first.click()
        page.get_by_role("option", name=ADRESS["pin"]).click()
        page.wait_for_timeout(1000)

        # ---- STREET ADDRESS ----
        page.get_by_role("combobox", name="Address Line").first.click()
        page.get_by_role("option", name=ADRESS["adrs"], exact=True).click()
        page.wait_for_timeout(1000)

        # ---- SAVE BUTTON ----
        address_save = page.locator("#save")
        if address_save.is_visible():
            address_save.click()
    else:
        print("Complete address already present — proceeding without changes.")