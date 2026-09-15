import SAP.sap_utils as sap

# pytest -s sap\test_travel.py
def test_travel(page):
    try:
        print("\n================ SAP - Travel Policy============")
        sap.url(page)
        user = sap.login(page)

        # -------- Storing of SAP Locator --------
        frame = page.locator("iframe[title='Application']").content_frame

        # ----- Contract start dates -----------
        sap.policy_dates(frame, page)

        # ------ Product ----
        sap.travel(frame, page)

        # ---- Policy Title -----
        sap.travel_title(frame)

        # ----- Policy Holder Level ------
        sap.travel_bp(frame, page)

        # ----- Contract -------
        product, contract_start = sap.travel_contract(frame, page)

        # ----- Coverage -----
        sap.travel_coverage(frame, page)

        # ----- Release Application -----
        sap.release(frame, page, product, contract_start, user)


    finally:    
        page.wait_for_timeout(3000)
        page.locator("#meAreaHeaderButton").click()
        page.get_by_text("Sign Out").click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(5000)