import re, os
from datetime import datetime
from dotenv import load_dotenv

DOWNLOADS_DIR = os.path.join(os.path.dirname(__file__),"NB", "downloads")

DATA = {}

def login(page):
    page.goto("https://agent-uat.tuneinsurance.com/")

    #  ------ Credentials -------
    load_dotenv()
    username = os.getenv("vijay")
    password = os.getenv("vij_pass")

    page.get_by_role("textbox", name="Username or email").fill(username)
    page.get_by_role("textbox", name="Password").fill(password)
    page.get_by_role("button", name="Login").click()
    print("Logged into: ", username)
    return username

def navigation(page):
    page.get_by_text("request_quote QMS Quotation").click()
    page.get_by_role("button", name="New Quote").click()
    page.wait_for_timeout(2000)
    page.get_by_role("heading", name="Motor").click()

def pc_moto(page):
    # === for Private car & Motorcycle ====
    page.get_by_role("heading", name="Reg. Motorcar/Motorcycle").click()
    page.get_by_role("button", name="Next").click()
    page.get_by_role("textbox").click()

def cv_moto(page):
    # === for commercial vehicle ====
    page.get_by_role("heading", name="Reg. Commercial Vehicle").click()
    page.get_by_role("button", name="Next").click()
    page.get_by_role("textbox").click()

def navi_pa(page):
    page.get_by_text("request_quote QMS Quotation").click()
    page.get_by_role("button", name="New Quote").click()
    page.get_by_role("heading", name="Personal Accident, Travel & Health").click()
    page.get_by_role("heading", name="Personal Accident", exact=True).click()
    page.get_by_role("button", name="Next").click()

def navi_dental(page):
    page.get_by_text("request_quote QMS Quotation").click()
    page.get_by_role("button", name="New Quote").click()
    page.get_by_role("heading",name="Personal Accident, Travel & Health").click()
    page.get_by_role("heading",name="Dental Shield").click()
    page.get_by_role("button",name="Next").click()

def endo_navigation(page, product):
    page.get_by_text("Policy Servicing (Endorsement)").click()
    print("Navigated to Endorsement Tile")
    # ---- Endorsement Product Selection ----
    page.locator(".mat-select-placeholder").click()

    # ---- Motor ----
    if product.lower() == "motor":
        page.get_by_role("option", name="Motor").click()
        print("**Performing Motor Endorsement**")

    # ---- Personal Accident ----
    elif product.lower() == "pa":
        page.get_by_role("option", name="Personal Accident").click()
        print("**Performing Personal Accident Endorsement**")

def incep_date(page):
    # today date
    today = datetime.today()
    # Angular Material aria-label format
    aria_date = today.strftime("%B %d, %Y").replace(" 0", " ")
    # Open calendar
    page.locator("mat-form-field").filter(has_text="Inception Date") .get_by_label("Open calendar").click()   
    # Select today
    page.get_by_role("gridcell", name=aria_date).click()
    inception_date = today.strftime("%d-%m-%Y")
    print("Inception Date: ", inception_date)

def start_date(page):
    # today date
    today = datetime.today()
    # Angular Material aria-label format
    aria_date = today.strftime("%B %d, %Y").replace(" 0", " ")
    # Open calendar
    page.locator("mat-form-field").filter(has_text="Start Date").get_by_label("Open calendar").click()   
    # Select today
    page.get_by_role("gridcell", name=aria_date).click()
    inception_date = today.strftime("%d-%m-%Y")
    print("Inception Date: ", inception_date)

def manager_approval(manager_page):
    load_dotenv()
    bm_user = os.getenv("bm_user")
    password = os.getenv("bm_pass")
    manager_page.get_by_role("textbox", name="Username or email").fill(bm_user)
    manager_page.get_by_role("textbox", name="Password").fill(password)
    manager_page.get_by_role("button", name="Login").click()
    manager_page.wait_for_timeout(25000)
    # === Approve the quote ===
    manager_page.get_by_role("button", name="Accept & Process").click()
    print("Manager approval done")
    manager_page.wait_for_timeout(10000)
    # --- Manager Logout ---
    manager_page.get_by_text(bm_user, exact=True).click()
    manager_page.get_by_text("Sign Out", exact=True).click()
    print("Terminated the Manager session")
    manager_page.wait_for_timeout(5000)
    manager_page.close()

def issue_policy(page):
        # === PROCEED TO POLICY ISSUANCE ===
        page.get_by_role("button", name="Proceed to Policy Issuance").click()

        # ==== POLICY ISSUANCE ====
        page.get_by_role("button", name="Issue Policy").click()
        print("Issue Policy button clicked")
        page.wait_for_timeout(30000)

        # ---- Wait until Policy number is released  ----
        max_wait = 100
        interval = 35
        elapsed = 0     
        policy_number = "-"

        while elapsed < max_wait:
            try:
                policy_element = page.locator("span.fw-bold").filter(has_text="Policy #:")
                policy_element.wait_for(state="visible", timeout=10000)
                policy_text = policy_element.inner_text().strip()
                policy_number = policy_text.replace("Policy #:", "").strip()
                if policy_number and policy_number != "-":
                    print("Policy Number:", policy_number)
                    break
                else:
                    print(f"Policy not yet issued, retrying... ({elapsed}s)")
            except:
                print(f"Policy locator not found, retrying... ({elapsed}s)")

            # Only reload if policy not found
            page.reload()
            ip = page.get_by_role("button", name="Issue Policy")
            if ip.is_visible():
                ip.click()
            page.wait_for_timeout(interval * 1000)
            elapsed += interval

        if policy_number == "-":
            print("Policy not issued after 2 minutes, something went wrong")

        DATA["policy"] = policy_number

        return policy_number

def quote_letter(page):
    # ---- Generate Quote Flow ----
    generate_quote_btn = page.get_by_role("button", name="Generate Quote")
    if generate_quote_btn.is_visible():
        generate_quote_btn.click()
        print("Clicked on Generate Quote button")

        with page.expect_download() as download_info:
            page.get_by_role("button", name="Submit").click()
        download_info.value.save_as(os.path.join(DOWNLOADS_DIR, "CV_quote.pdf"))

def policy_letter(page):
    # ---- Download the policy schedule ----
    page.get_by_role("button", name="Download & e-mail Policy").click()
    page.wait_for_timeout(5000)

    with page.expect_download() as download_info:
        page.get_by_role("button", name="Submit").click()
    download = download_info.value
    download.save_as(os.path.join(DOWNLOADS_DIR, "CV_policy.pdf"))

    print("Policy is Issued and Schedule letter downloaded successfully.")

# ---- Premiums -----
def extract_myr(text: str) -> float:
    is_negative = "-" in text
    match = re.search(r"[\d,]+\.?\d*", text)
    value = float(match.group().replace(",", "")) if match else 0.0
    return -value if is_negative else value

def motor_prem(page):

    # ---- Premiums ----
    sum_insured1 = page.locator("li").filter(has_text="Vehicle Sum Insured").locator(".summary-result-value").inner_text().strip()
    sum_insured = extract_myr(sum_insured1)

    ap = page.locator("li").filter(has_text="Act Premium").locator(".summary-result-value").inner_text().strip()
    act_prem = extract_myr(ap)

    bp = page.locator("li").filter(has_text="Basic Premium").locator(".summary-result-value").inner_text().strip()
    basic_prem = extract_myr(bp)

    ncd_value = page.locator("(//li[contains(.,'NCD')]//span[contains(@class,'summary-result-value')])[1]").inner_text().strip()
    ncd = extract_myr(ncd_value)

    ncd_after = page.locator("li").filter(has_text="Premium after NCD").locator(".summary-result-value").inner_text().strip()
    after_ncd = extract_myr(ncd_after)

    gp = page.locator("li").filter(has_text="Gross Premium").locator(".summary-result-value").inner_text().strip()
    gross_premium =  extract_myr(gp)

    tax = page.locator("li").filter(has_text="SST").locator(".summary-result-value").inner_text().strip()
    sst = extract_myr(tax)

    sd = page.locator("li").filter(has_text="Stamp Duty").locator(".summary-result-value").inner_text().strip()
    stamp_duty = extract_myr(sd)

    total_payable = page.locator("div").filter(has_text="Total Payable Premium").locator(".final-amount").inner_text().strip()
    total = extract_myr(total_payable)

    # ---- TIPS Premium ----
    print(f"Sum Insured         : {sum_insured}")
    print(f"Act Premium         : {act_prem}")
    print(f"Basic Premium       : {basic_prem}")
    print(f"NCD Premium         : {ncd}")
    print(f"Premium after NCD   : {after_ncd}")
    print(f"Gross Premium       : {gross_premium}")
    print(f"SST                 : {sst}")
    print(f"Stamp Duty          : {stamp_duty}")
    print(f"Total Premium       : {total}")

    # --- Stroing values ---
    DATA["act_prem"]     = act_prem
    DATA["gross_prem"]   = gross_premium
    DATA["sst"]          = sst
    DATA["stamp_duty"]   = stamp_duty
    DATA["total_prem"]   = total

    return sum_insured, act_prem, basic_prem, ncd, after_ncd, gross_premium, sst, stamp_duty, total

def pa_prem(page):
    value = page.locator("li").filter(has_text="Sum Insured").locator(".summary-result-value").inner_text().strip()
    sum_insured = extract_myr(value)
    print("\nSum Insured:", sum_insured)

    gp = page.locator("li").filter(has_text="Gross Premium").locator(".summary-result-value").inner_text().strip()
    gross_premium = extract_myr(gp)
    print("Gross Premium:", gross_premium)

    try:
        re = page.locator("li").filter(has_text="Rebate").locator(".summary-result-value").inner_text().strip()
        rebate = extract_myr(re)
        print("Rebate:", rebate)
    except:
        rebate = None  
        print("No Rebate")

    tax = page.locator("li").filter(has_text="SST").locator(".summary-result-value").inner_text().strip()
    sst = extract_myr(tax)
    print("SST:", sst)

    sd = page.locator("li").filter(has_text="Stamp Duty").locator(".summary-result-value").inner_text().strip()
    stamp_duty = extract_myr(sd)
    print("Stamp Duty:", stamp_duty)

    total_payable = page.locator("div").filter(has_text="Total Payable Premium").locator(".final-amount").inner_text().strip()
    total = extract_myr(total_payable)
    print("Total Premium:", total)

    return sum_insured, gross_premium, rebate, sst, stamp_duty, total

def dental_prem(page):
    gp = page.locator("li").filter(has_text="Gross Premium").locator(".summary-result-value").inner_text().strip()
    gross_premium = extract_myr(gp)
    print("Gross Premium:", gross_premium)

    re = page.locator("li").filter(has_text="Rebate").locator(".summary-result-value").inner_text().strip()
    rebate = extract_myr(re)
    print("Rebate:", rebate)

    tax = page.locator("li").filter(has_text="SST").locator(".summary-result-value").inner_text().strip()
    sst = extract_myr(tax)
    print("SST:", sst)

    sd = page.locator("li").filter(has_text="Stamp Duty").locator(".summary-result-value").inner_text().strip()
    stamp_duty = extract_myr(sd)
    print("Stamp Duty:", stamp_duty)

    total_payable = page.locator("div").filter(has_text="Total Payable Premium").locator(".final-amount").inner_text().strip()
    total = extract_myr(total_payable)
    print("Total Premium:", total)

    return gross_premium, rebate, sst, stamp_duty, total 