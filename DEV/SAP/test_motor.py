import SAP.sap_utils as sap

def test_mc(page):
    try:
        print("\n================ SAP - MC Policy============")
        sap.url(page)
        sap.login(page)

        # -------- Storing of SAP Locator --------
        frame = page.locator("iframe[title='Application']").content_frame

        # -------- Policy Dates --------
        sap.policy_dates(frame, page)

        # -------- Product --------
        sap.mc_product(frame, page)

        # -------- BP & Commission Contract --------
        sap.bp(frame, page)

        # -------- Contract Level --------
        contract_start = sap.mc_contract(frame, page)

        # -------- Coverage Type --------
        sap.mc_coverage(frame, page)

        # -------- Release Application ----------
        sap.release(frame, page, "MC", contract_start)
        page.pause()

    finally:
        page.wait_for_timeout(3000)
        page.locator("#meAreaHeaderButton").click()
        page.get_by_text("Sign Out").click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(5000)

def test_pc(page):
    try:
        print("\n================ SAP - PC Policy============")
        sap.url(page)
        sap.login(page)

        # ----- Storing of SAP Locator --------
        frame = page.locator("iframe[title='Application']").content_frame

        # ----------- Policy Dates --------
        sap.policy_dates(frame, page)

        # -------- Product --------
        sap.pc_product(frame, page)

        # ----- BP & Commission Contract ------
        sap.bp(frame, page)

        # -------- Contract Level --------
        contract_start = sap.pc_contract(frame, page)

        # -------- Coverage Type --------------
        sap.pc_coverage(frame, page)

        # -------- Release Application --------
        sap.release(frame, page, "PC", contract_start)

    finally:
        page.wait_for_timeout(3000)
        page.locator("#meAreaHeaderButton").click()
        page.get_by_text("Sign Out").click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(5000)