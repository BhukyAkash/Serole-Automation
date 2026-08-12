import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from base_login import manager_approval

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
                f"https://agent-uat.tuneinsurance.com/#/qms/quote/motor/{url_segment}/cover-details"
                f"?edit=true&quoteNr={quote_number}"
            )
            manager_approval(manager_page)

            # ---- Back button in Agent ----
            page.get_by_role("button", name="Back").click()
            print("Navigated to Back for Quote letter")
            page.wait_for_timeout(3000)

        # === Quote Status - Referred ======
        elif status == "Referred":
            # ---- Submission Number ----
            submission_no = (page.locator("div.-first").filter(has_text="Submission #").locator("div.summary-result").nth(1).text_content().strip())
            print("Submission Number: ", submission_no)

            # --- SAP Browser Launch ----
            browser = page.context.browser
            sap_context = browser.new_context(no_viewport=True)
            sap_page = sap_context.new_page()

            # ---- Import of SAP - PQM ----
            uw = UW_SAP()
            # --- First login ----
            uw.first_login(sap_page)
            # --- Second login ----
            uw.second_login(sap_page)
            # --- Navigation to Underwriting Worklist ----
            sap_uw_page1 = uw.navigate_to_uw(sap_page)
            # --- Search of Submission number ----
            uw.approving(sap_uw_page1, submission_no)
            # ---- Logout of PQM ---
            uw.pqm_logout(sap_uw_page1)
            # --- Logout of PM ----
            uw.pm_logout(sap_page)
            page.wait_for_timeout(3000)

            # ---- Back button in Agent ----
            page.get_by_role("button", name="Back").click()
            print("Navigated to Back for Quote letter")
            page.wait_for_timeout(5000)
            page.get_by_role("button", name="Next").click()
            page.wait_for_timeout(5000)

        # === For Other Status ====
        else:
            print(status)
        
    # ---- Quote status printing -----
    re_status =  page.locator("dx-status span[dxstatuschip]").inner_text().strip()
    print("After approval Quote Status:", re_status)

def pa_nstp_flow(page, quote_number):

    submit_approval_btn = page.get_by_role("button", name="Submit for TPM Staff Approval")
    # ---- Submit for TPM staff approval button -----
    if submit_approval_btn.is_visible():
        submit_approval_btn.click()
        print("Clicked on Submit for TPM Staff Approval button")
        page.wait_for_timeout(25000)

        page.wait_for_function("""
        () => {
            const status = document.querySelector("span.mx-2");
            return status &&
                (status.textContent.includes("Referred") ||
                    status.textContent.includes("Submitted For Review"));
        }
        """, timeout=60000)

        # ---- Quote status printing -----
        status = page.locator("span.mx-2").inner_text().strip()
        print("Quote Status: ", status)

        # === Quote Status - Submitted For Review ======
        if status == "Submitted For Review":
            browser = page.context.browser
            manager_context = browser.new_context(no_viewport = True)
            manager_page = manager_context.new_page()
            manager_page.goto(f"https://agent-uat.tuneinsurance.com/#/qms/quote/medical/personal/verify?edit=true&quoteNr={quote_number}")

            manager_approval(manager_page)

            # ---- Back button in Agent ----
            page.get_by_role("button", name="Back").click()
            print("Navigated to Back for Quote letter")
            page.wait_for_timeout(3000)

        # === Quote Status - Referred ======
        elif status == "Referred":
            # ---- Submission Number ----
            submission_no = (page.locator("div.-first").filter(has_text="Submission #").locator("div.summary-result").nth(1).text_content().strip())
            print("Submission Number: ", submission_no)

            # --- SAP Browser Launch ----
            browser = page.context.browser
            sap_context = browser.new_context(no_viewport=True)
            sap_page = sap_context.new_page()

            # ---- Import of SAP - PQM ----
            uw = UW_SAP()
            # --- First login ----
            uw.first_login(sap_page)
            # --- Second login ----
            uw.second_login(sap_page)
            # --- Navigation to Underwriting Worklist ----
            sap_uw_page1 = uw.navigate_to_uw(sap_page)
            # --- Search of Submission number ----
            uw.approving(sap_uw_page1, submission_no)
            # ---- Logout of PQM ---
            uw.pqm_logout(sap_uw_page1)
            # --- Logout of PM ----
            uw.pm_logout(sap_page)
            page.wait_for_timeout(3000)

            # ---- Back button in Agent ----
            page.get_by_role("button", name="Back").click()
            print("Navigated to Back for Quote letter")
            page.wait_for_timeout(5000)
            page.get_by_role("button", name="Next").click()
            page.wait_for_timeout(5000)

        # === For Other Status ====
        else:
            pass


class UW_SAP:
    def first_login(self, page):
        page.wait_for_load_state("networkidle")
        page.goto("https://tus4appuat.tuneprotect.com:44303/sap/bc/ui2/flp#Shell-home")
        page.get_by_role("textbox", name="User").click()
        page.get_by_role("textbox", name="User").fill("UWTEAM2")
        page.get_by_role("textbox", name="Password").click()
        page.get_by_role("textbox", name="Password").fill("Quality@12345")
        page.get_by_role("button", name="Log On").click()

    def second_login(self, page):
        page.get_by_label("User").fill("UWTEAM2")
        page.get_by_label("Password").fill("Quality@12345")
        page.get_by_role("button", name="Log On").click()
        page.wait_for_load_state("networkidle")

    def navigate_to_uw(self, page):
        page.get_by_label("Group Navigation").get_by_text("Quotation Management").click()
        with page.expect_popup() as page1_info:
            page.get_by_role("link", name="My Underwriting Worklist Extn").click()
        page1 = page1_info.value
        page.wait_for_timeout(5000)
        return page1

    def approving(self, page1, submission_no):
        page1.wait_for_load_state("networkidle")
        page1.get_by_role("cell", name=submission_no).click()
        page1.wait_for_load_state("networkidle")
        page1.get_by_role("button", name="Underwrite").click()
        page1.get_by_role("button", name="Multi Select").click()
        page1.get_by_role("button", name="Select All", exact=True).click()
        page1.get_by_role("button", name="Assign to Me").click()
        page1.get_by_role("button", name="Accept").click()
        page1.get_by_role("button", name="OK").click()
        print("Approved the quote in PQM")

    def pqm_logout(self, page1):
        page1.get_by_role("button", name="Profile of UWTEAM2 UWTEAM2").click()
        page1.get_by_text("Sign Out").click()
        page1.get_by_role("button", name="OK").click()
        page1.wait_for_timeout(5000)
        page1.close()

    def pm_logout(self, page):
        page.get_by_role("button", name="Profile of UWTEAM2 UWTEAM2").click()
        page.get_by_text("Sign Out").click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(5000)
        page.close()