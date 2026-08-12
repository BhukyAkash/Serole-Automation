import os
from datetime import datetime
from .vehicle_info import info, get_vehicle_info
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

def system_date():
    return datetime.now().strftime("%d.%m.%y")

def policy_dates(frame, page):
    today = system_date()
    # today = info["date"]

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

    # --------- Year of Manufacturer ----------
    manufacturer = frame.locator("input[title*='Construction Year of Vehicle']")
    expect(manufacturer).not_to_have_value("", timeout=30000)
    manufacture_year = int(manufacturer.input_value())
    age = datetime.now().year - manufacture_year

    if age >= 15:
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

def mc_coverage(frame, page):
    info = get_vehicle_info("MC")
    # ------------ Coverage -------------
    covpac = info["covpac"]
    page.wait_for_timeout(3000)
    frame.get_by_text(covpac).dblclick()
    frame.get_by_text(covpac, exact=True).click()
    page.wait_for_timeout(2000)
    frame.get_by_text(covpac, exact=True).dblclick()

    # -------- Limit / Deductible --------
    frame.get_by_role("tab", name="Limit/Deductible").click()

    field = frame.locator("span[id$='#1,2#if']")
    sum_insured = field.inner_text().strip()

    if float(sum_insured.replace(",", "")) == 0:
        page.wait_for_timeout(1000)
        field.dblclick()
        frame.locator("input[data-hint*='ABCALIMIT-LIMIT_AM']").fill(info["si"])
        page.wait_for_timeout(1000)
        page.keyboard.press("F8")

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
    covpac = info["covpac"]    # "Third Party, Fire & Theft"
    page.wait_for_timeout(3000)
    frame.get_by_text(covpac).dblclick()
    frame.get_by_text(covpac, exact=True).click()
    page.wait_for_timeout(2000)
    frame.get_by_text(covpac, exact=True).dblclick()

    # -------- Limit / Deductible --------
    frame.get_by_role("tab", name="Limit/Deductible").click()

    field = frame.locator("span[id$='#1,2#if']")
    sum_insured = field.inner_text().strip()

    if float(sum_insured.replace(",", "")) == 0:
        page.wait_for_timeout(1000)
        field.dblclick()
        frame.locator("input[data-hint*='ABCALIMIT-LIMIT_AM']").fill(info["si"])
        page.wait_for_timeout(1000)
        page.keyboard.press("F8")

    if covpac == "comprehensive":
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

def release(frame, page, product, contract_start):
    # -------- Policy Number --------
    page.wait_for_timeout(1000)
    policy_number = frame.locator("input[title*='Policy Number']").input_value()
    print(f"Policy Number - {policy_number}")

    # -------- Store Policy Number --------
    today = datetime.now().strftime("%d.%m.%y")
    with open(r"SAP\policy_numbers.txt", "a") as file:
        file.write(f"{product} - {policy_number} - {contract_start} - {today}\n")

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