import pytest
from playwright.sync_api import sync_playwright
import os
from NB.utils.network_logs import NetworkLogger

# -------- Register custom markers (avoids PytestUnknownMarkWarning) --------
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "no_network_logger: skip network logger summary for this test"
    )

# -------- Custom Command Line Arguments --------
def pytest_addoption(parser):
    parser.addoption(
        "--product",
        action="store",
        default="motor",
        help="Product type: Motor or Personal Accident"
    )

# -------- Playwright Fixture with Tracing --------
@pytest.fixture(scope="function")
def page(request):
    TRACES_DIR = os.path.join(os.path.dirname(__file__), "traces")
    os.makedirs(TRACES_DIR, exist_ok=True)

    test_file = os.path.splitext(os.path.basename(request.node.fspath))[0]
    trace_path = os.path.join(TRACES_DIR, f"{test_file}.zip")

    print(f"\n[TRACE] Saving trace to: {trace_path}")

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False, args=["--start-maximized"])
        context = browser.new_context(no_viewport=True)

        context.tracing.start(
            screenshots=True,
            snapshots=True,
            sources=True
        )

        page = context.new_page()

        # ---- Attach network logger (captures bp, ncdRequestV2, quote responses) ----
        page.net_logger = NetworkLogger(page)
        page.playwright = playwright  # expose driver so other browsers can be launched safely

        yield page

        # ---- Skip network logger summary for tests marked "no_network_logger" ----
        if "no_network_logger" not in [mark.name for mark in request.node.iter_markers()]:
            page.net_logger.summary()

        context.tracing.stop(path=trace_path)

        context.clear_cookies()
        context.close()
        browser.close()

'''
# -------- Screenshot if test fails --------

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page", None)

        if page:
            os.makedirs("screenshots", exist_ok=True)
            screenshot_path = f"screenshots/{item.name}.png"
            page.screenshot(path=screenshot_path)
            print(f"\n[SCREENSHOT] Saved to: {screenshot_path}")'''