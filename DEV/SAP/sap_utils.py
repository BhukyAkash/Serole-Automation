import os
from datetime import datetime
from .vehicle_info import info, get_vehicle_info
from .travel_info import air_aisa
from playwright.sync_api import expect
from dotenv import load_dotenv

def url(page):
    page.goto("https://tus4appdev.tuneprotect.com:44300/sap/bc/ui2/flp#ZPM_SEM_OBJ-display")

def login(page):
    load_dotenv()
    user = os.getenv("apasha")
    password = os.getenv("apa_pass")

    page.wait_for_load_state("networkidle")
    page.get_by_label("User").fill(user)                 # "APASHA" 
    page.get_by_label("Password").fill(password)
    page.get_by_role("button", name="Log On").click()
    page.wait_for_load_state("networkidle")

    return user

def system_date():
    return datetime.now().strftime("%d.%m.%Y")

def policy_dates(frame, page):
    # today = system_date()
    today = info["date"]

    frame.get_by_role("textbox", name="Policy Start Required").click()
    frame.get_by_role("textbox", name="Policy Start Required").fill(today)

    frame.get_by_role("textbox", name="Submission To PP Date Required").click()
    frame.get_by_role("textbox", name="Submission To PP Date Required").fill(today)

    frame.get_by_role("textbox", name="Received Date Required").click()
    frame.get_by_role("textbox", name="Received Date Required").fill(today)

def mc_product(frame, page):
    frame.get_by_role("textbox", name="Sales Prod.Templ.ID Required").click()
    frame.get_by_role("textbox", name="Sales Prod.Templ.ID Required").fill(info["MC"]["pm_id"])

    page.wait_for_timeout(1000)
    page.keyboard.press("Enter")

    frame.get_by_role("textbox", name="Acquisition Type Required").click()
    frame.get_by_role("option", name="New Business").click()

    page.keyboard.press("F8")

def pc_product(frame, page):
    frame.get_by_role("textbox", name="Sales Prod.Templ.ID Required").click()
    frame.get_by_role("textbox", name="Sales Prod.Templ.ID Required").fill(info["PC"]["pm_id"])

    page.wait_for_timeout(1000)
    page.keyboard.press("Enter")

    frame.get_by_role("textbox", name="Acquisition Type Required").click()
    frame.get_by_role("option", name="New Business").click()

    page.keyboard.press("F8")

def bp(frame, page):

    # ---------- Business Partner --------
    frame.get_by_role("button", name="Detail").click()
    frame.get_by_role("textbox", name="Business Partner Required").click()
    frame.get_by_role("textbox", name="Business Partner Required").fill(info["BP"])
    page.keyboard.press("F8")

    # --------- Commission Contract -------
    frame.get_by_role("tab", name="Commission").click()
    page.wait_for_timeout(1000)
    frame.get_by_role("button", name="Add").click()
    frame.get_by_role("textbox", name="Comm. Contract No.").click()
    frame.get_by_role("textbox", name="Comm. Contract No.").fill(info["CC"])
    page.keyboard.press("F8")

    frame.get_by_role("button", name="Complete Business Transaction").click()

def mc_contract(frame, page):
    info = get_vehicle_info("MC")
    # ----------- CONTRACT LEVEL ------------
    page.wait_for_timeout(3000)
    frame.get_by_text("Motorcycle", exact=True).nth(1).dblclick()
    frame.get_by_label("Level 2 Expanded").get_by_text("Motorcycle").click()
    frame.get_by_label("Level 2 Expanded").get_by_text("Motorcycle").dblclick()

    # --------- Contract Data ---------
    frame.get_by_role("textbox", name="Coverage Type Required").click()
    frame.get_by_role("option", name=info["coverage_type"]).click()

    end_date = frame.locator("input[title='End date']").input_value()
    contract_start = frame.locator("input[title='Technical Contract Start']").input_value()
    print(f"Contract Start Date: {contract_start} | End Date: {end_date}")

    # --------- RISK Insured Object ---------
    frame.get_by_role("tab", name="Risk").click()
    frame.get_by_role("button", name="Detail").click()
    frame.get_by_role("button", name="Create").click()
    frame.get_by_role("textbox", name="Vehicle reg. no.").click()
    frame.get_by_role("textbox", name="Vehicle reg. no.").fill(info["vehicle_no"])
    frame.get_by_role("textbox", name="Vehicle reg. no.").press("Enter")
    page.wait_for_timeout(3000)

    frame.get_by_role("textbox", name="Vehicle Usage").click()
    frame.get_by_role("textbox", name="Vehicle Usage").fill("011")

    # --------- Year of Manufacturer ----------
    coverage_type = info["coverage_type"]
    if coverage_type == "Comprehensive":
        manufacturer = frame.locator("input[title*='Construction Year of Vehicle']")
        expect(manufacturer).not_to_have_value("", timeout=30000)
        manufacture_year = int(manufacturer.input_value())
        age = datetime.now().year - manufacture_year
        if age >= 15:
            manufacturer.fill("2020")
        else:
            pass
    else:
        pass

    # ----- Duplicate Issuance ----
    page.wait_for_timeout(2000)
    page.keyboard.press("Control+S")
    try:
        frame.get_by_role("button", name="Yes").click(timeout=3000)
    except:
        pass
    frame.get_by_role("button", name="Complete").click()
    page.wait_for_timeout(2000)
    try:
        frame.get_by_role("button", name="Yes").click(timeout=3000)
    except:
        pass

    # -------- Vehicle Info Review -----------
    seat = frame.locator("input[title*='Seating Capacity']")
    seat.fill("2")
    page.wait_for_timeout(1000)
    sc = seat.input_value()
    engine_capacity = frame.locator("input[title*='ENGINE capacity']").input_value()
    print(f"Engine Capacity: {engine_capacity} | Seating Capacity: {sc}" )
    frame.get_by_role("textbox", name="Unit Type Required").click()
    frame.get_by_role("option", name="CC CC").click()

    # -------- Complete Business Transaction --------
    page.wait_for_timeout(1000)
    page.keyboard.press("F8")
    page.wait_for_timeout(1000)
    frame.get_by_role("button", name="Complete Business Transaction").click()
    return contract_start

def mc_coverage(frame, page):
    info = get_vehicle_info("MC")
    # ------------ Coverage -------------
    covpac = info["coverage_type"]
    page.wait_for_timeout(3000)
    frame.get_by_text(covpac).dblclick()
    frame.get_by_text(covpac, exact=True).click()
    page.wait_for_timeout(2000)
    frame.get_by_text(covpac, exact=True).dblclick()

    # -------- Limit / Deductible --------
    if covpac != "Third Party Liability":
        frame.get_by_role("tab", name="Limit/Deductible").click()

        field = frame.locator("span[id$='#1,2#if']")
        sum_insured = field.inner_text().strip()

        if float(sum_insured.replace(",", "")) == 0:
            page.wait_for_timeout(1000)
            field.dblclick()
            frame.locator("input[data-hint*='ABCALIMIT-LIMIT_AM']").fill(info["si"])
            page.wait_for_timeout(1000)
            page.keyboard.press("F8")
    else:
        pass

    # -------- Complete Business Transaction --------
    page.wait_for_timeout(1000)
    frame.get_by_role("button", name="Complete Business Transaction").click()

def pc_contract(frame, page):
    info = get_vehicle_info("PC")
    # ----------- CONTRACT LEVEL ------------
    product = "Private Car"
    page.wait_for_timeout(3000)
    frame.get_by_text(product, exact=True).dblclick()
    frame.get_by_label("Level 2 Expanded").get_by_text(product).click()
    frame.get_by_label("Level 2 Expanded").get_by_text(product).dblclick()

    # --------- Contract Data - Coverage ---------
    frame.get_by_role("textbox", name="Coverage Type Required").click()
    frame.get_by_role("option", name=info["coverage_type"]).click()

    end_date = frame.locator("input[title='End date']").input_value()
    contract_start = frame.locator("input[title='Technical Contract Start']").input_value()
    print(f"Contract Start Date: {contract_start} | End Date: {end_date}")

    # --------- RISK Insured Object ---------
    frame.get_by_role("tab", name="Risk").click()

    frame.get_by_role("button", name="Detail").click()
    frame.get_by_role("button", name="Create").click()
    frame.get_by_role("textbox", name="Vehicle reg. no.").click()
    frame.get_by_role("textbox", name="Vehicle reg. no.").fill(info["vehicle_no"])
    frame.get_by_role("textbox", name="Vehicle reg. no.").press("Enter")
    page.wait_for_timeout(3000)

    # ----- Vehicle Details ------
    frame.get_by_role("textbox", name="Vehicle Usage").click()
    frame.get_by_role("textbox", name="Vehicle Usage").fill("001")
    frame.get_by_role("textbox", name="Chassis No").click()
    frame.get_by_role("textbox", name="Chassis No").fill("AKASH78901")
    frame.get_by_role("textbox", name="Year of Manufacture").click()
    frame.get_by_role("textbox", name="Year of Manufacture").fill("2020")
    frame.get_by_role("textbox", name="Vehicle Class").click()
    frame.get_by_role("textbox", name="Vehicle Class").fill("002")
    frame.get_by_role("textbox", name="Make").click()
    frame.get_by_role("textbox", name="Make").fill("055")
    frame.get_by_role("textbox", name="Model").click()
    frame.get_by_role("textbox", name="Model").fill("023")
    frame.get_by_role("textbox", name="Model").press("Enter")

    # --------- Year of Manufacturer ----------
    manufacturer = frame.locator("input[title*='Construction Year of Vehicle']")
    expect(manufacturer).not_to_have_value("", timeout=30000)
    manufacture_year = int(manufacturer.input_value())
    age = datetime.now().year - manufacture_year

    if age >= 20:
        manufacturer.fill("2020")
    else:
        pass

    page.wait_for_timeout(2000)
    page.keyboard.press("Control+S")
    try:
        frame.get_by_role("button", name="Yes").click(timeout=3000)
    except:
        pass
    frame.get_by_role("button", name="Complete").click()
    page.wait_for_timeout(2000)
    try:
        frame.get_by_role("button", name="Yes").click(timeout=3000)
    except:
        pass
    # -------- Vehicle Info Review -----------
    engine_no = frame.get_by_role("textbox", name="Engine No Required")
    if not engine_no.input_value():
        engine_no.fill("ANANTHA12345")

    engine_capacity = frame.get_by_role("textbox", name="Engine capacity Required")
    if not engine_capacity.input_value():
        engine_capacity.fill("1500")

    frame.get_by_role("textbox", name="Safety Features Required").click()
    frame.get_by_role("option", name="ABS (No Airbags)").click()
    page.wait_for_timeout(1000)
    frame.get_by_role("textbox", name="Anti-Theft Required").click()
    frame.get_by_role("option", name="002 Alarm w Immobilizer").click()
    page.wait_for_timeout(1000)
    frame.get_by_role("textbox", name="Garaged Required").click()
    frame.get_by_role("option", name="003 Locked Compound").click()

    # ------- Seating and Engine Capacity ---------
    seat = frame.locator("input[title*='Seating Capacity']")
    seat.fill("2")
    page.wait_for_timeout(1000)
    sc = seat.input_value()
    engine_capacity = frame.locator("input[title*='ENGINE capacity']").input_value()
    print(f"Engine Capacity: {engine_capacity} | Seating Capacity: {sc}" )
    frame.get_by_role("textbox", name="Unit Type Required").click()
    frame.get_by_role("option", name="CC CC").click()
    page.wait_for_timeout(1000)
    page.keyboard.press("F8")
    page.wait_for_timeout(1000)
    frame.get_by_role("button", name="Complete Business Transaction").click()
    return contract_start

def pc_coverage(frame, page):
    info = get_vehicle_info("PC")
    # ------------ Coverage -------------
    covpac = info["coverage_type"]
    page.wait_for_timeout(3000)
    frame.get_by_text(covpac).dblclick()
    frame.get_by_text(covpac, exact=True).click()
    page.wait_for_timeout(2000)
    frame.get_by_text(covpac, exact=True).dblclick()

    # -------- Limit / Deductible --------
    if covpac != "Third Party Liability":
        frame.get_by_role("tab", name="Limit/Deductible").click()

        field = frame.locator("span[id$='#1,2#if']")
        sum_insured = field.inner_text().strip()

        if float(sum_insured.replace(",", "")) == 0:
            page.wait_for_timeout(1000)
            field.dblclick()
            frame.locator("input[data-hint*='ABCALIMIT-LIMIT_AM']").fill(info["si"])
            page.wait_for_timeout(1000)
            page.keyboard.press("F8")
    else:
        pass

    if covpac == "Comprehensive":
        # ---------- Clause - Named Driver ----------
        frame.get_by_role("tab", name="Clause").click()
        page.wait_for_timeout(1000)
        frame.locator("div[lsdata*='btnCMD_F_CLAUSE_ADD']").click()
        frame.get_by_role("textbox", name="Clause").click()
        page.wait_for_timeout(1000)
        frame.get_by_role("option", name="Named Driver").click()
        frame.get_by_role("button", name="Create").click()
        page.wait_for_timeout(1000)
        cell = frame.locator("span[id$='#1,1#if']")
        cell.click()
        page.keyboard.type("NAMED DRIVER")
        page.keyboard.press("Enter")

    # -------- Complete Business Transaction --------
    page.wait_for_timeout(1000)
    frame.get_by_role("button", name="Complete Business Transaction").click()

def release(frame, page, product, contract_start, user):
    # -------- Policy Number --------
    page.wait_for_timeout(1000)
    policy_number = frame.locator("input[title*='Policy Number']").input_value()
    print(f"Policy Number - {policy_number}")

    # -------- Save / Check / Calculate / Release --------
    page.wait_for_timeout(1000)
    frame.get_by_role("button", name="Save  Emphasized").click()

    page.wait_for_timeout(1000)
    frame.get_by_role("button", name="Check").click()

    page.wait_for_timeout(3000)
    frame.get_by_role("button", name="Calculate Application").click()

    page.wait_for_timeout(3000)
    frame.get_by_role("button", name="Release Application").click()
    page.wait_for_timeout(1000)
    frame.get_by_role("button", name="Continue Release").click()

    page.wait_for_timeout(3000)
    frame.get_by_role("button", name="Continue Release").click()

    page.wait_for_timeout(13000)
    # -------- Check BadJPJ Request --------
    bad_jpj = frame.get_by_text("BadJPJ Request")

    if bad_jpj.is_visible():
        print("BadJPJ Request found - Policy NOT saved")
    else:
        # -------- Store Policy Number --------
        today = datetime.now().strftime("%d.%m.%y")
        with open(r"SAP\policy_numbers.txt", "a") as file:
            file.write(f"{product} - {policy_number} - {contract_start} - {today} - {user}\n")

        print("Policy stored in text file")

# ========== TRAVEL - AIR ASIA ==========
master = air_aisa["travel"].get("masterPolicy")
def travel(frame, page):
    frame.get_by_role("textbox", name="Sales Prod.Templ.ID Required").click()
    frame.get_by_role("textbox", name="Sales Prod.Templ.ID Required").fill(air_aisa["travel"]["pm_id"])

    page.keyboard.press("Enter")

    if master :
        frame.get_by_role("textbox", name="Master Policy Number").click()
        frame.get_by_role("textbox", name="Master Policy Number").fill(master)

    page.wait_for_timeout(1000)
    page.keyboard.press("Enter")
    page.wait_for_timeout(3000)
    page.keyboard.press("F8")
    return master

def travel_title(frame):
    frame.get_by_role("textbox", name="Policy Title Required").click()
    frame.get_by_text(air_aisa["travel"]["policy_title"], exact=True).click()

    today = datetime.now().strftime("%Y%m%d")
    if master:
        frame.get_by_role("textbox", name="External Reference").click()
        frame.get_by_role("textbox", name="External Reference").fill(f"AK-{today}")

def travel_bp(frame, page):
    if not master :
        # ---------- Business Partner --------
        frame.get_by_role("button", name="Detail").click()
        frame.get_by_role("textbox", name="Business Partner Required").click()
        frame.get_by_role("textbox", name="Business Partner Required").fill(air_aisa["BP"])
        page.keyboard.press("F8")

        # --------- Commission Contract -------
        frame.get_by_role("tab", name="Commission").click()
        page.wait_for_timeout(1000)
        frame.get_by_role("button", name="Add").click()
        frame.get_by_role("textbox", name="Comm. Contract No.").click()
        frame.get_by_role("textbox", name="Comm. Contract No.").fill(air_aisa["CC"])
        page.keyboard.press("F8")

        frame.get_by_role("button", name="Complete Business Transaction").click()

def scroll_and_click_nav_cell(frame, page, cell_name, dblclick=True, max_scrolls=10, scroll_amount=-300, label=None):
    tree_area = frame.get_by_text("FS-PM Navigation Tree")
    box = tree_area.bounding_box()
    if box:
        page.mouse.move(box["x"] + 50, box["y"] + 100)

    for _ in range(max_scrolls):
        cell = frame.get_by_label(label).get_by_text(cell_name, exact=True) if label else frame.get_by_text(cell_name, exact=True)
        if cell.count() > 0 and cell.first.is_visible():
            cell.first.click()
            if dblclick:
                cell.first.dblclick()
            return
        page.mouse.wheel(0, scroll_amount)
        page.wait_for_timeout(300)

    raise Exception(f"Could not find '{cell_name}' in nav tree after scrolling")

def travel_contract(frame, page):
    page.wait_for_timeout(3000)
    product = "Travel"

    frame.get_by_text("Travel", exact=True).dblclick()
    scroll_and_click_nav_cell(frame, page, product, label="Level 2 Expanded")

    # --------- Contract Duration---------
    end_date = frame.locator("input[title='End date']").input_value()
    contract_start = frame.locator("input[title='Technical Contract Start']").input_value()
    print(f"Contract Start Date: {contract_start} | End Date: {end_date}")

    if master:
        frame.get_by_role("textbox", name="Travel Destination").click()
        frame.get_by_text("Inbound", exact=True).click()

        frame.get_by_role("textbox", name="Trip").click()
        frame.get_by_text("One Way", exact=True).click()

        frame.get_by_role("textbox", name="Depature Country").click()
        frame.get_by_text("Andorra", exact=True).click()

    # ===== Risk - IO Level ========
    frame.get_by_role("tab", name="Risk").click()
    frame.get_by_role("button", name="Detail").click()
    frame.get_by_role("textbox", name="Business Partner").fill("1000025326")
    frame.get_by_role("button", name="Copy  Emphasized").click()
    frame.get_by_role("tab", name="Premium").click()
    page.wait_for_timeout(3000)
    frame.get_by_role("textbox", name="Premium Type").click()
    frame.get_by_text("OneTime Premium", exact=True).click()
    frame.get_by_role("button", name="Create").click()
    page.wait_for_timeout(3000)
    page.keyboard.press("F8")

    return product, contract_start

def travel_coverage(frame, page):
    coverage = air_aisa["travel"]["coverage"]
    page.wait_for_timeout(3000)
    frame.get_by_text(coverage, exact=True).dblclick()
    page.wait_for_timeout(2000)
    scroll_and_click_nav_cell(frame, page, coverage)

    # ========= Limit/Deductible =========
    frame.get_by_role("tab", name="Limit/Deductible").click()
    frame.locator('span[id$="#1,2#if"]').dblclick()
    frame.get_by_role("textbox", name="Limit Amount(SI)").click()
    frame.get_by_role("textbox", name="Limit Amount(SI)").fill(air_aisa["travel"]["si"])
    frame.get_by_role("button", name="Copy  Emphasized").click()
    frame.get_by_role("button", name="Complete Business Transaction").click()
    frame.get_by_role("button", name="Save  Emphasized").click()