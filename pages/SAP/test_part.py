from test_bp import test_bp_pc, test_bp_mc
import pytest
from playwright.sync_api import sync_playwright

# pytest -s SAP\test_part.py
@pytest.mark.no_network_logger
def test_part(page):

    # First browser
    test_bp_pc(page)

    # ---- SAP Inquiry (Browser 2) ----
    sap_browser = page.playwright.chromium.launch(headless=False, args=["--start-maximized"])
    sap_context = sap_browser.new_context(no_viewport=True)
    sap_page = sap_context.new_page()

    test_bp_mc(sap_page)

    sap_context.close()
    sap_browser.close()
    