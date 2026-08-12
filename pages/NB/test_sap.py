from playwright.sync_api import sync_playwright
import pytest

from NB.test_mc import test_mc_motor
from NB.test_pc import test_pc_motor
from NB.test_cv import test_cv_motor
from base_login import DATA

# pytest -s nb\test_sap.py::TestPC
class TestPC:
    def test_car(self, page):

        # ---- PC Automate (Browser 1 - TIPS, relaunched) ----
        try:
            test_pc_motor(page)
            policy = DATA["policy"]
            print(f"Motor Car Policy: {policy}")

            # ---- SAP Inquiry (Browser 2) ----
            sap_browser = page.playwright.chromium.launch(headless=False, args=["--start-maximized"])
            sap_context = sap_browser.new_context(no_viewport=True)
            sap_page = sap_context.new_page()

            TestSAP().test_sap(sap_page)

            sap_context.close()
            sap_browser.close()

        except Exception as e:
            print("Test failed: ", e)

        # ---- MC Automate (Browser 1 - TIPS, relaunched) ----
        try:
            test_mc_motor(page)
            policy = DATA["policy"]
            print(f"Motor Cycle Policy: {policy}")

            # ---- SAP Inquiry (Browser 2) ----
            sap_browser = page.playwright.chromium.launch(headless=False, args=["--start-maximized"])
            sap_context = sap_browser.new_context(no_viewport=True)
            sap_page = sap_context.new_page()

            TestSAP().test_sap(sap_page)

            sap_context.close()
            sap_browser.close()

        except Exception as e:
            print("Test failed: ", e)

        # ---- CV Automate (Browser 1 - TIPS) ----
        try:
            test_cv_motor(page)
            policy = DATA["policy"]
            print(f"Commercial Vehicle Policy: {policy}")

            # DATA["policy"] = "402000072760"
            # DATA["act_prem"] = 364.32
            # DATA["gross_prem"] = 709.47
            # DATA["sst"] = 56.76
            # DATA["stamp_duty"] = 10.0
            # DATA["total_prem"] = 808.63
            # policy = DATA["policy"]
            # print(f"Motor Car Policy: {policy}")

            # ---- SAP Inquiry (Browser 2) ----
            TestSAP().test_sap(page)

        except Exception as e:
            print("Test failed: ", e)

@pytest.mark.no_network_logger
class TestSAP:
    def first_login(self, page):
        page.wait_for_load_state("networkidle")
        page.goto("https://tus4appuat.tuneprotect.com:44303/sap/bc/ui2/flp#Shell-home")
        page.get_by_role("textbox", name="User").click()
        page.get_by_role("textbox", name="User").fill("SSANTHOSH")
        page.get_by_role("textbox", name="Password").click()
        page.get_by_role("textbox", name="Password").fill("Quality@12345")
        page.get_by_role("button", name="Log On").click()

    def second_login(self, page):
        page.get_by_label("User").fill("SSANTHOSH")
        page.get_by_label("Password").fill("Quality@12345")
        page.get_by_role("button", name="Log On").click()
        page.wait_for_load_state("networkidle")

    def scroll_and_click_tree_cell(self, page, frame, cell_name, dblclick=True, max_scrolls=10, scroll_amount=300):
        tree_area = frame.get_by_text("FS-PM Navigation Tree")
        box = tree_area.bounding_box()

        if box:
            page.mouse.move(box["x"] + 50, box["y"] + 100)

        for _ in range(max_scrolls):
            cell = frame.get_by_role("cell", name=cell_name)
            if cell.count() > 0:
                try:
                    if cell.first.is_visible():
                        if dblclick:
                            cell.first.dblclick()
                        else:
                            cell.first.click()
                        return
                except:
                    pass
            page.mouse.wheel(0, scroll_amount)
            page.wait_for_timeout(300)

        raise Exception(f"Could not find '{cell_name}'")

    @staticmethod
    def pm_logout(self, page, page1=None):
        try:
            # Logout from SAP
            page.get_by_role("button", name="Profile of Siluveru Santhosh").click()
            page.get_by_text("Sign Out").click()
            page.get_by_role("button", name="OK").click()
            page.wait_for_load_state("networkidle")
        except Exception as e:
            print(f"Logout failed: {e}")

        finally:
            # Close Inquiry popup
            if page1:
                try:
                    page1.close()
                except:
                    pass

            # Close main SAP page
            try:
                page.close()
            except:
                pass

    def test_sap(self, page):
        
        try:
            TestSAP.first_login(self, page)
            TestSAP.second_login(self, page)
            print("In SAP Screen")

            page.get_by_label("Group Navigation").get_by_text("POLICY-MANAGEMENT").click()
            print("Navigated to Policy Management")
            with page.expect_popup() as page1_info:
                page.get_by_role("link", name="Inquiry").click()
            page1 = page1_info.value
            print("In Inquiry Tile")

            frame = page1.frame_locator('iframe[title="Application"]')

            policy = DATA["policy"]

            frame.get_by_role("textbox", name="Policy Number").fill(policy)
            page1.keyboard.press("Enter")

            page1.wait_for_timeout(3000)
            page1.keyboard.press("F8")
            page1.wait_for_timeout(3000)

            # ==== Posting Data ====
            TestSAP.scroll_and_click_tree_cell(self, page1, frame, "Posting Data")
            page1.wait_for_timeout(2000)

            frame.locator('input[title="Settlement To"]').fill("31.12.2029")

            dropdown_btn = frame.locator("[id='M0:46:2:1:2B256:1::3:17-btn']")
            dropdown_btn.click()
            frame.get_by_role("option", name="All", exact=True).click()
            page.wait_for_timeout(1000)

            refresh = frame.locator('[id="M0:46:2:1:2B256:1::3:76"]')
            refresh.click()
            page.wait_for_timeout(1000)

            frame.get_by_text("Application Number").nth(2).click()
            frame.get_by_label("Document header").get_by_role("button", name="Sort in Ascending Order").click()
            page.wait_for_timeout(1000)

            # ==== Posting Cells =====
            act = frame.locator('[id*="1,5#if"]').first
            act_cell = act.inner_text(timeout=5000).strip()

            total = frame.locator('[id*="2,5#if"]').first
            total_cell = total.inner_text(timeout=5000).strip()

            sd_cell = frame.locator('[id*="3,5#if"]').first.inner_text(timeout=5000).strip()

            incep_cell = frame.locator('[id*="1,7#if"]').first.inner_text(timeout=5000).strip()

            end_cell = frame.locator('[id*="1,8#if"]').first.inner_text(timeout=5000).strip()

            total.dblclick()
            page.wait_for_timeout(2000)

            gross_cell = frame.locator('[id*="C263#1,4#if"]').first
            gross = gross_cell.inner_text(timeout=5000).strip()

            sst_cell = frame.locator('[id*="C263#2,4#if"]').first
            sst = sst_cell.inner_text(timeout=5000).strip()

            # ==== Collections/Disbursements ====
            TestSAP.scroll_and_click_tree_cell(self, page1, frame, "Collections/Disbursements")
            page1.wait_for_timeout(1000)
            frame.locator('span[title="Current Premium Balance"]').last.click()
            page1.wait_for_timeout(1000)
            frame.locator('div[title="Total"]').nth(1).click()
            page1.wait_for_timeout(2000)

            # --- Last row CD premium ---
            cd_cells = frame.locator("[id*=',4#if']")
            count = cd_cells.count()
            cd = ""
            for i in range(count - 1, -1, -1):
                text = cd_cells.nth(i).inner_text(timeout=2000).strip()
                if text:
                    cd = text
                    break

            # ==== Commissions ====
            TestSAP.scroll_and_click_tree_cell(self, page1, frame, "Commission")
            page1.wait_for_timeout(1000)
            frame.locator('span[title="PartRemAmnt in CMC"]:visible').click()
            page1.wait_for_timeout(1000)
            frame.locator('div[title="Total"]').nth(1).click()
            page1.wait_for_timeout(2000)

            # --- Last row ICM premium ---
            icm_cells = frame.locator("[id*=',12#if']")
            count = icm_cells.count()
            icm = ""
            for i in range(count - 1, -1, -1):
                text = icm_cells.nth(i).inner_text(timeout=2000).strip()
                if text:
                    icm = text
                    break

            
            print(f"Inception Date   : {incep_cell}")
            print(f"End Date         : {end_cell}")

            DATA["act_premium"]     = act_cell
            DATA["gross_premium"]   = gross
            DATA["tax"]             = sst
            DATA["stamp"]           = sd_cell
            DATA["total_premium"]   = total_cell
            DATA["collection"]      = cd
            DATA["comission"]       = icm

            # --- Premium Comparison ---
            TestSAP.sap_prem(self, page)

        except Exception as e:
            print(f"Test failer: {e}")


        finally:
            TestSAP.pm_logout(page, page1)

    def sap_prem(self, page):
        act_cell    = DATA["act_premium"]
        gross       = DATA["gross_premium"]
        sst         = DATA["tax"]
        sd_cell     = DATA["stamp"]
        total_cell  = DATA["total_premium"]
        cd          = DATA["collection"]
        icm         = DATA["comission"]


        print(f"SAP Act Premium  : {act_cell}")
        print(f"SAP Gross Premium: {gross}")
        print(f"SAP SST          : {sst}")
        print(f"SAP Stamp Duty   : {sd_cell}")
        print(f"Total Premium    : {total_cell}")
        print(f"CD Postings      : {cd}")
        print(f"ICM Postings     : {icm}")

        tips_act = float(DATA["act_prem"])
        sap_act = float(act_cell.replace(",", ""))
        if tips_act == sap_act:
            print("✅ Act Premium matched")
        else:
            print(f"❌ Act Premium not matched, TIPS = {tips_act} | SAP = {sap_act}")

        tips_gross = float(DATA["gross_prem"])
        sap_gross = float(gross.replace(",", ""))
        if tips_gross == sap_gross:
            print("✅ Gross Premium matched")
        else:
            print(f"❌ Gross Premium not matched, TIPS = {tips_gross} | SAP = {sap_gross}")

        tips_sst = float(DATA["sst"])
        sap_sst = float(sst.replace(",", ""))
        if tips_sst == sap_sst:
            print("✅ SST matched")
        else:
            print(f"❌ SST not matched, TIPS = {tips_sst} | SAP = {sap_sst}")

        tips_sd = float(DATA["stamp_duty"])
        sap_sd = float(sd_cell.replace(",", ""))
        if tips_sd == sap_sd:
            print("✅ Stamp Duty matched")
        else:
            print(f"❌ Stamp Duty not matched, TIPS = {tips_sd} | SAP = {sap_sd}")

        tips_total = float(DATA["total_prem"])
        sap_cd = float(cd.replace(",", ""))
        if tips_total == sap_cd:
            print("✅ CD (Total Premium) matched")
        else:
            print(f"❌ CD (Total Premium) not matched, TIPS = {tips_total} | SAP = {sap_cd}")

        expec_icm = round(tips_gross * 0.1, 2)
        sap_icm = float(icm.replace(",", ""))
        if expec_icm == sap_icm:
            print("✅ ICM Premium matched")
        else:
            print(f"❌ ICM Premium not matched, Expected = {expec_icm} | SAP = {sap_icm}")