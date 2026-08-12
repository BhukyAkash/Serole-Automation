# ------ PC Extensions ------
def pc_extension(page, coverage_type, flags):

    page.get_by_role("button", name="Extension Coverage").click()

    # --- Package Type Selection ----
    if flags["select_autobuddy"]:
        page.get_by_text("NAPackage Type").click()
        page.wait_for_timeout(1000)
        page.get_by_role("option", name="Motor Shield").click()   #Autobuddy  #Motor Shield
        page.wait_for_timeout(1000)
        # --- Selected Package type ----
        selected_package = page.locator("#mat-select-value-11 span.mat-select-min-line").inner_text()
        print("Selected Package:", selected_package)

        if "Autobuddy" in selected_package:
            page.locator(".mat-select-placeholder").first.click()
            page.wait_for_timeout(2000)
            plan = "PLAN A"
            page.get_by_role("option", name=plan).click()
            print("Plan Type:", plan)
        else:
            print("Motor shield Package Selected")
        
    else:
        print("No Autobuddy package selected")

    page.wait_for_timeout(3000)
    # ---- Extensions ----
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

        for extension_name in extensions:
            page.locator("span").filter(has_text=extension_name).get_by_role("button").click()

            if extension_name == "Windscreen Damage":
                page.locator(".additional-benefit", has_text="Windscreen Damage").locator("input#sumInsured:not([readonly])").fill("800")

            elif extension_name == "Inclusion of Special Perils":
                page.get_by_label("Extension Coverage").get_by_text("Vehicle Sum Insured", exact=True).click()

            print(f"{extension_name} selected successfully")

    else:
        print("No extensions selected")

# ------ MC Extensions ------
def mc_extension(page, coverage_type, flags):

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

# ------ CV Extensions ------
def cv_extension(page, coverage_type, flags):

    page.get_by_role("button", name="Extension Coverage").click()

    # --- Package Type Selection ----
    if flags["select_autobuddy"]:
        page.get_by_text("NAPackage Type").click()
        page.wait_for_timeout(1000)
        page.get_by_role("option", name="Motorist PA").click()
        page.wait_for_timeout(1000)
        selected_package = page.locator("#packageType .mat-select-min-line").inner_text()
        print("Selected Package:", selected_package)

        if "Motorist PA" in selected_package:
            page.locator(".mat-select-placeholder").first.click()
            plan = "PLAN D"
            page.get_by_role("option", name=plan).click()
        else:
            print("Motorist PA not selected → skipping PLAN selection")
        print("Plan Type:", plan)
    else:
        print("Motorist PA package is not selected")

    # ---- Extensions ----
    if flags["select_extensions"]:
        if coverage_type == "Comprehensive":
            extensions = [
                "Windscreen Damage",
                "Strike riot and civil commotion",
                "Ferry Transit to and / or from Sabah and Labuan",
                "Inclusion of Special Perils",
                "Passenger Risk",
                "Passenger Risk-Employees of the Insured-good carrying vehicle only",
            ]
        elif coverage_type == "TP, Fire & Theft":
            extensions = [
                "Passenger Risk",
                "Passenger Risk-Employees of the Insured-good carrying vehicle only",
            ]
        elif coverage_type == "Third Party":
            extensions = [
                "Passenger Risk",
                "Passenger Risk-Employees of the Insured-good carrying vehicle only",
            ]

        for extension_name in extensions:
            page.locator("span").filter(has_text=extension_name).get_by_role("button").click()

            if extension_name == "Windscreen Damage":
                page.locator("mat-form-field").filter(has_text="Sum Insured").locator("#sumInsured").fill("800")

            print(f"{extension_name} selected successfully")
    else:
        print("No extensions selected")