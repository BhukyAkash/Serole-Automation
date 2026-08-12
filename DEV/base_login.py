import os
from dotenv import load_dotenv
from datetime import datetime

def login(page):
    page.goto("https://tune.dev.indigit.io/#/home#Agent")
    load_dotenv()
    dev_user = os.getenv("dev_user")
    dev_pass = os.getenv("dev_pass")
    page.get_by_role("textbox", name="Username or email").fill(dev_user)
    page.get_by_role("textbox", name="Password").fill(dev_pass)
    page.get_by_role("button", name="Login").click()
    print("\nLogged into:", dev_user)

def navigation(page):
    page.get_by_text("request_quote QMS Quotation").click()
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
    page.get_by_role("heading", name="Personal Accident, Travel & Health").click()
    page.get_by_role("heading", name="Personal Accident", exact=True).click()
    page.get_by_role("button", name="Next").click()

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

def manager_approval(manager_page):
    load_dotenv()
    dev_user = os.getenv("dev_bm")
    dev_pass = os.getenv("dev_bm_pass")
    manager_page.get_by_role("textbox", name="Username or email").fill(dev_user)
    manager_page.get_by_role("textbox", name="Password").fill(dev_pass)
    manager_page.get_by_role("button", name="Login").click()
    manager_page.wait_for_timeout(25000)
    # === Approve the quote ===
    manager_page.get_by_role("button", name="Accept & Process").click()
    print("Manager approval done")
    manager_page.wait_for_timeout(10000)
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
            page.wait_for_timeout(interval * 1000)
            elapsed += interval

        if policy_number == "-":
            print("Policy not issued after 2 minutes, something went wrong")

        return policy_number

def nstp_flow(page, quote_number, vehicle_type):

    submit_approval_btn = page.get_by_role("button", name="Submit for TPM Staff Approval")

    # ---- Upload Doc later (PC only) ----
    if vehicle_type == "pc" or vehicle_type == "mc":
        upload_later = page.get_by_text("Upload Supporting documents later").first
        try:
            upload_later.wait_for(state="visible", timeout=5000)
            if upload_later.is_enabled():
                upload_later.click()
                page.locator("dx-evidence-upload").get_by_role("textbox").click()
                page.locator("dx-evidence-upload").get_by_role("textbox").fill("will upload documents later")
                print("NSTP - Upload later of Documents")
            else:
                print("STP case - Upload later disabled, skipping")
        except:
            print("Upload later option not present, skipping")

    # ---- Submit for TPM staff approval button -----
    if submit_approval_btn.is_visible():
        submit_approval_btn.click()
        print("Clicked on Submit for TPM Staff Approval button")
        page.wait_for_timeout(25000)

        page.wait_for_function("""
        () => {
            const status = document.querySelector("dx-status");
            return status &&
                (status.innerText.includes("Referred") ||
                    status.innerText.includes("Submitted For Review"));
        }
        """, timeout=60000)

        # ---- Quote status printing -----
        status = page.locator("dx-status a").inner_text().strip()
        print("Quote Status: ", status)

        # === Quote Status - Submitted For Review ======
        if status == "Submitted For Review":
            browser = page.context.browser
            manager_context = browser.new_context(no_viewport = True)
            manager_page = manager_context.new_page()

            url_segment = "reg" if vehicle_type in ("pc", "mc") else "rcv"
            manager_page.goto(
                f"https://tune.dev.indigit.io/#/qms/quote/motor/{url_segment}/cover-details?edit=true&quoteNr={quote_number}"
            )
            manager_approval(manager_page)

            # ---- Back button in Agent ----
            page.get_by_role("button", name="Back").click()
            print("Navigated to Back for Quote letter")
            page.wait_for_timeout(3000)

        # === For Other Status ====
        else:
            print(status)
        
    # ---- Quote status printing -----
    re_status =  page.locator("dx-status span[dxstatuschip]").inner_text().strip()
    print("After approval Quote Status:", re_status)