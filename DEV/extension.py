from datetime import datetime

AUTOMATION_FLAGS = {

    "MC": {
        "explore_extensions":   True,
        "select_autobuddy":     False,
        "select_extensions":    False,
    },

    "PC": {
        "explore_extensions":   True,
        "select_autobuddy":     False,
        "select_extensions":    False,
    },

    "CV": {
        "explore_extensions":   True,
        "select_autobuddy":     False,
        "select_extensions":    False,
    },
}

# ------ PC Extensions ------
def pc_extension(page, coverage_type):
    flags = AUTOMATION_FLAGS["PC"]

    print("======== Extension Coverage Selection ========")
    page.get_by_role("button", name="Extension Coverage").click()

    # --- Package Type Selection ----
    if flags["select_autobuddy"]:
        page.get_by_text("NAPackage Type").click()
        page.wait_for_timeout(1000)
        page.get_by_role("option", name="Motor Shield").click() #Autobuddy #Motor Shield
        page.wait_for_timeout(1000)

        selected_package = page.locator("#mat-select-value-11 span.mat-select-min-line").inner_text()
        print("Selected Package:", selected_package)

        if "Autobuddy" in selected_package:
            page.locator(".mat-select-placeholder").first.click()
            page.get_by_role("option", name="PLAN A").click()
        else:
            print("Autobuddy not selected → skipping PLAN selection")
    else:
        pass

    # ---- Individual Extensions ----
    if flags["select_extensions"]:
        if coverage_type == "Comprehensive":
            extensions = [
                "check All Drivers",
                "Windscreen Damage",
                "Inclusion of Special Perils",
                "Legal Liability to Passenger (LLP)",
                "Legal Liability to Third Party caused by Passenger",
                "Strike Riot and Civil Commotions",
                "Ferry Transit to and / or from Sabah and Labuan"
            ]
        elif coverage_type == "TP, Fire & Theft":
            extensions = [
                "Legal Liability to Passenger (LLP)",
                "Legal Liability to Third Party caused by Passenger"
            ]
        else:
            extensions = []

        for extension_name in extensions:
            page.locator("span").filter(has_text=extension_name).get_by_role("button").click()

            if extension_name == "Windscreen Damage":
                page.locator("mat-form-field").filter(has_text="Sum Insured *MYR").locator("#sumInsured").fill("800")
            elif extension_name == "Inclusion of Special Perils":
                page.get_by_label("Extension Coverage").get_by_text("Vehicle Sum Insured", exact=True).click()

            print(f"{extension_name} selected successfully")
    else:
        pass

# ------ MC Extensions ------
def mc_extension(page, coverage_type):
    flags = AUTOMATION_FLAGS["MC"]

    print("======== Extension Coverage Selection ========")
    page.get_by_role("button", name="Extension Coverage").click()

    # --- Package Type Selection ----
    if flags["select_autobuddy"]:
        page.get_by_text("NAPackage Type").click()
        page.wait_for_timeout(1000)
        page.get_by_role("option", name="Motorcyclist PA").click()
        page.wait_for_timeout(1000)
        selected_package = page.locator("#mat-select-value-11 span.mat-select-min-line").inner_text()
        print("Selected Package:", selected_package)

        if "Motorcyclist PA" in selected_package:
            page.locator(".mat-select-placeholder").first.click()
            page.wait_for_timeout(2000)
            plan = "PLAN A"
            page.get_by_role("option", name=plan).click()
            print("Plan Type:", plan)
        else:
            print("Motorcyclist PA not selected → skipping PLAN selection")
    else:
        print("MPA Contract not selected")

    # ---- Extensions ----
    if flags["select_extensions"]:
        if coverage_type == "Comprehensive":
            extensions = [
                "All Riders",
                "Inclusion of Special Perils",
                "Legal Liability to Pillion",
                "Accessories fixed to motorcycle",
                "Ferry Transit to and / or from Sabah and Labuan",
                "Strike Riot and Civil Commotion",
            ]
        elif coverage_type == "Third Party":
            extensions = [
                "All Riders",
            ]

        for extension_name in extensions:
            page.locator("span").filter(has_text=extension_name).get_by_role("button").click()

            if extension_name == "Accessories fixed to motorcycle":
                container = page.locator(".additional-benefit-wrapper").filter(has_text=extension_name)
                container.locator("input#sumInsured").fill("800")

            print(f"{extension_name} selected successfully")
    else:
        print("No extensions selected")

def cv_trailer(page):
    page.get_by_role("button", name="Add add").click()
    page.locator("mat-form-field").filter(has_text="Trailer # *").locator("#vehicleRegNo").fill("123211")
    page.locator("mat-form-field").filter(has_text="Chassis # *").locator("#vehicleChassisNo").fill("124346256")

    page.locator("mat-select#vehicleMake").first.click()
    page.get_by_role("option", name="VOLVO").click()

    page.locator("mat-select#model").click()
    page.get_by_role("option", name="PAVERS").click()

    page.locator("mat-select#yearOfManufacture").click()
    page.get_by_role("option", name="2024").click()

    page.locator("mat-form-field").filter(has_text="Carrying Capacity *").locator("#carryingCapacity").fill("11")

    page.locator("mat-select#tonnesAndKilograms").click()
    page.get_by_role("option", name="Kg").click()

    page.locator("mat-select#carriageGoods").click()
    page.get_by_role("option", name="General Cargo").click()

    page.locator("mat-select#coverType").click()
    page.get_by_role("option", name="Comprehensive").click()

    today = datetime.today().strftime("%d-%m-%Y")
    page.locator("app-trailer-attachment input#inceptionDate").fill(today)

    page.locator("mat-form-field").filter(has_text="Trailer Sum Insured *MYR").locator("#marketValue").click()
    page.locator("mat-form-field").filter(has_text="Trailer Sum Insured *MYR").locator("#marketValue").fill("10000")

    page.keyboard.press("Tab")

    page.locator("app-trailer-attachment").get_by_role("button", name="Save").click()
