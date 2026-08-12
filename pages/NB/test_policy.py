

# # ============ SAMPLE FILE FOR PRACTICE ===========


import re, pytest
import time
from vehicle_info import get_vehicle_info, ADRESS

# @pytest.mark.no_network_logger
# def test_policy(page):
#     try:
#         quote_num = 1000070608
#         page.goto(f"https://agent-uat.tuneinsurance.com/#/qms/quote/motor/reg/cover-details?edit=true&quoteNr=1000071123")
#         # page.goto("https://agent-uat.tuneinsurance.com/#/qms/quote/medical/personal/additional-info?edit=true&quoteNr=1000070940")
#         username = "playwright.test@serole.com"   #"vijaykumar.likki@serole.com"
#         page.get_by_role("textbox", name="Username or email").fill(username) 
#         page.get_by_role("textbox", name="Password").fill("Serole@321")
#         page.get_by_role("button", name="Login").click()
#         page.wait_for_load_state("networkidle")

#         page.wait_for_timeout(5000)
#         address_start_time = time.time()

#         # ---- Quote status printing -----
#         re_status =  page.locator("dx-status span[dxstatuschip]").inner_text().strip()
#         print("After approval Quote Status:", re_status)

#         address_end_time = time.time()
#         print(f"[TIMING] Policyholder address section took {address_end_time - address_start_time:.2f} seconds")


#         # # ========= FIRST SCREEN ===========
#         # vehicle_info = get_vehicle_info("PC")
        
#         # # ---- VEHICLE REG ----
#         # data = "WMY1618"
#         # page.get_by_role("textbox").first.fill(data)

#         # # ---- PLACE OF USE ----
#         # page.locator(".mat-select-placeholder").click()
#         # page.get_by_role("option", name=vehicle_info["place_of_use"]).click()

#         # # ---- VEHICLE SEARCH ----
#         # page.get_by_role("button", name="search Vehicle Search").click()
#         # page.wait_for_timeout(5000)

#         # try:
#         #     page.get_by_role("menuitem", name="edit").click(timeout=3000)
#         #     page.get_by_role("button", name="Proceed").click()
#         # except:
#         #     pass

#         # # ---- MAKE ----
#         # make_dropdown = page.locator("mat-select#make")
#         # if vehicle_info["change_vehicle"]:
#         #     if make_dropdown.is_visible():
#         #         make_dropdown.click()
#         #         page.get_by_role("option", name=vehicle_info["make"]).click()
#         #         page.wait_for_timeout(1000)
#         #     else:
#         #         print("Make dropdown not visible, skipping")
#         # else:
#         #     pass

#         # # ---- MODEL ----
#         # model_dropdown = page.locator("mat-select#model")
#         # if vehicle_info["change_vehicle"]:
#         #     if model_dropdown.is_visible():
#         #         model_dropdown.click()
#         #         page.get_by_role("option", name=vehicle_info["model"]).click()
#         #         page.wait_for_timeout(1000)
#         #     else:
#         #         print("Model dropdown not visible, skipping")
#         # else:
#         #     pass

#         # # ---- YEAR ----
#         # year_dropdown = page.locator("mat-select#year")
#         # if vehicle_info["change_vehicle"]:
#         #     if year_dropdown.is_visible():
#         #         year_dropdown.click()
#         #         page.get_by_role("option", name=vehicle_info["year"]).click()
#         #     else:
#         #         pass
#         # else:
#         #     pass

#         # # ---- READ BACK FOR LOGGING ----
#         # make  = page.locator("#make .mat-select-min-line").inner_text()
#         # model = page.locator("#model .mat-select-min-line").inner_text()
#         # year  = page.locator("#year .mat-select-min-line").inner_text()
#         # print(f"Make: {make} | Model: {model} | Year: {year}")

#         # # ---- ENGINE CAPACITY ----
#         # cc_input = page.locator('input#cc')
#         # if cc_input.is_visible():
#         #     current_value = cc_input.input_value().strip()
#         #     if current_value == "" or current_value == "0":
#         #         cc_input.dblclick()
#         #         cc_input.fill(vehicle_info["engine_capacity"])
#         #         print(f"Engine Capacity: {vehicle_info['engine_capacity']}")
#         #     else:
#         #         print(f"Engine Capacity set: {current_value}")

#         # # ---- SEATING CAPACITY ----
#         # seat_input = page.locator('input#seatCapacity')
#         # if seat_input.is_visible():
#         #     current_value = seat_input.input_value().strip()
#         #     if current_value == "" or current_value == "0":
#         #         seat_input.dblclick()
#         #         seat_input.fill(vehicle_info["seating_capacity"])
#         #         print(f"Seating Capacity: {vehicle_info['seating_capacity']}")
#         #     else:
#         #         print(f"Seating Capacity set: {current_value}")

#         # sc = page.locator('input#seatCapacity').input_value().strip()
#         # cc = page.locator('input#cc').input_value().strip()
#         # print(f"Engine & Seating Capacity: {cc} || {sc}")


#         # # ---- SAVE VEHICLE INFO ----
#         # search_vehicle = page.get_by_role("button", name="Save Vehicle Info").first
#         # try:
#         #     search_vehicle.wait_for(state="visible", timeout=5000)
#         #     search_vehicle.click()
#         #     page.wait_for_load_state("networkidle")
#         # except:
#         #     print("Save Vehicle Info button not available")

#         # page.wait_for_timeout(5000)
#         # values = page.locator("span.status-text").all_inner_texts()
#         # print(values)

#         # # ========== SECOND SCREEN ==========

#         # # ---- COVERAGE TYPE ----
#         # coverage = page.locator("#mat-select-value-9")
#         # if vehicle_info["change_coverage"]:
#         #     if coverage.is_visible():
#         #         coverage.click()
#         #         page.get_by_role("option", name=vehicle_info["coverage_type"]).click()
#         #         page.wait_for_timeout(1000)
#         #         print(f"Coverage selected: {vehicle_info['coverage_type']}")
#         #     else:
#         #         print("coverage dropdown not visible, skipping")
#         # else:
#         #     pass

#         # # ---- MARKET VALUE ----
#         # market_value_text = page.locator("mat-form-field").filter(has_text="Market Value").locator("#ismMarketValue").input_value().strip()
#         # market_value = int(float(market_value_text.replace(",", "")))
#         # print(f"Market Value: {market_value}")

#         # # ----- Agreed Value ------
#         # page.wait_for_timeout(2000)
#         # page.get_by_text("Agreed Value").click()
#         # page.wait_for_timeout(2000)

#         # # ------ Adjust Agreed Value ------
#         # page.get_by_text("Adjust Agreed Value").click()
#         # agreed_value_field = page.locator("mat-form-field").filter(has_text="Agreed Value % *percent Edit").locator("#agreedValue")

#         # # ---- FILL CUSTOM PERCENTAGE ----
#         # custom_percent = 22
#         # agreed_value_field.click()
#         # agreed_value_field.fill(str(custom_percent))

#         # # ---- CONFIRM FILLED VALUE TOOK EFFECT ----
#         # updated_percent_text = agreed_value_field.input_value().strip()
#         # updated_percent = int(float(updated_percent_text))
#         # assert updated_percent == custom_percent, (f"Expected Agreed Value % to be updated to {custom_percent}, but got {updated_percent}")
#         # print(f"✅ Agreed Value % successfully updated to: {updated_percent}")

#         # # ---- TRIGGER RECALCULATION ----
#         # page.get_by_role("button", name="Extension Coverage").click()

#         # sum_text = page.locator("mat-form-field").filter(has_text="Vehicle Sum Insured").locator("#sumInsured").input_value().strip()
#         # actual_sum = int(float(sum_text.replace(",","")))
#         # print(f"Sum Insured after Agreed Value: {actual_sum}")

#         # hints = page.locator("dx-hint div")
#         # for i in range(hints.count()):
#         #     text = hints.nth(i).inner_text().strip()
#         #     print("Condition:", text)

#         # print("====== Verification of SI =====")

#         # # ---- EXPECTED CALCULATION (uses the ACTUAL filled percent) ----
#         # mv_decimal = Decimal(str(market_value))
#         # multiplier = Decimal("1") + (Decimal(str(custom_percent)) / Decimal("100"))
#         # before_round = mv_decimal * multiplier

#         # # Correct ceiling to nearest hundred
#         # expected_sum = int((before_round / 100).to_integral_value(rounding=ROUND_CEILING) * 100)

#         # print(f"Sum Insured before round off ({market_value} * {multiplier}): {before_round}")
#         # print("Sum Insured After round off:", expected_sum)

#         # # ---- VERIFICATION ----
#         # assert actual_sum == expected_sum, (
#         #     f"Sum Insured mismatch! Market Value={market_value}, Agreed Value%={custom_percent}, "
#         #     f"Raw(MV*{multiplier})={before_round}, Expected(rounded up to nearest 100)={expected_sum}, "
#         #     f"Actual displayed={actual_sum}"
#         # )

#         # print(f"✅ PASS: Sum Insured correctly rounded up to nearest hundred. "
#         #     f"MV={market_value}, Agreed Value%={custom_percent} → Expected={expected_sum}, Actual={actual_sum}")


#         # # ---- Premiums ----
#         # sum_insured = page.locator("li").filter(has_text="Vehicle Sum Insured").locator(".summary-result-value").inner_text().strip()
#         # value = extract_myr(sum_insured)
#         # print("\nSum Insured:", value)

#         # ap = page.locator("li").filter(has_text="Act Premium").locator(".summary-result-value").inner_text().strip()
#         # act_prem = extract_myr(ap)
#         # print("Act Premium:", act_prem)

#         # bp = page.locator("li").filter(has_text="Basic Premium").locator(".summary-result-value").inner_text().strip()
#         # basic_prem = extract_myr(bp)
#         # print("Basic Premium:", basic_prem)

#         # ncd_value = page.locator("(//li[contains(.,'NCD')]//span[contains(@class,'summary-result-value')])[1]").inner_text().strip()
#         # ncd = extract_myr(ncd_value)
#         # print("NCD Premium:", ncd)

#         # ncd_after = page.locator("li").filter(has_text="Premium after NCD").locator(".summary-result-value").inner_text().strip()
#         # after_ncd = extract_myr(ncd_after)
#         # print("Premium after NCD:", after_ncd)

#         # gp = page.locator("li").filter(has_text="Gross Premium").locator(".summary-result-value").inner_text().strip()
#         # gross_premium = extract_myr(gp)
#         # print("Gross Premium:", gross_premium)

#         # tax = page.locator("li").filter(has_text="SST").locator(".summary-result-value").inner_text().strip()
#         # sst = extract_myr(tax)
#         # print("SST:", sst)

#         # sd = page.locator("li").filter(has_text="Stamp Duty").locator(".summary-result-value").inner_text().strip()
#         # stamp_duty = extract_myr(sd)
#         # print("Stamp Duty:", stamp_duty)

#         # total_payable = page.locator("div").filter(has_text="Total Payable Premium").locator(".final-amount").inner_text().strip()
#         # total = extract_myr(total_payable)
#         # print("Total Premium:", total)

#     finally:
#         page.get_by_text(username , exact=True).click()
#         page.get_by_text("Sign Out", exact=True).click()
#         page.wait_for_timeout(3000)


# def first_login(page):
#     page.wait_for_load_state("networkidle")
#     page.goto("https://tus4appuat.tuneprotect.com:44303/sap/bc/ui2/flp#Shell-home")
#     page.get_by_role("textbox", name="User").click()
#     page.get_by_role("textbox", name="User").fill("SSANTHOSH")
#     page.get_by_role("textbox", name="Password").click()
#     page.get_by_role("textbox", name="Password").fill("Quality@12345")
#     page.get_by_role("button", name="Log On").click()

# def second_login(page):
#     page.get_by_label("User").fill("SSANTHOSH")
#     page.get_by_label("Password").fill("Quality@12345")
#     page.get_by_role("button", name="Log On").click()
#     page.wait_for_load_state("networkidle")

# def scroll_and_click_tree_cell(page, frame, cell_name,dblclick=True,max_scrolls=10,scroll_amount=300):

#     tree_area = frame.get_by_text("FS-PM Navigation Tree")
#     box = tree_area.bounding_box()

#     if box:
#         page.mouse.move(box["x"] + 50, box["y"] + 100)

#     for _ in range(max_scrolls):

#         cell = frame.get_by_role("cell", name=cell_name)

#         if cell.count() > 0:
#             try:
#                 if cell.first.is_visible():
#                     if dblclick:
#                         cell.first.dblclick()
#                     else:
#                         cell.first.click()
#                     return
#             except:
#                 pass

#         page.mouse.wheel(0, scroll_amount)
#         page.wait_for_timeout(300)

#     raise Exception(f"Could not find '{cell_name}'")

# def pm_logout(page1):
#     page1.get_by_role("button", name="Profile of Siluveru Santhosh").click()
#     page1.get_by_text("Sign Out").click()
#     page1.get_by_role("button", name="OK").click()

# @pytest.mark.no_network_logger
# def test_inquiry(page):

#     try:
#         first_login(page)
#         second_login(page)

#         page.get_by_label("Group Navigation").get_by_text("POLICY-MANAGEMENT").click()
#         with page.expect_popup() as page1_info:
#             page.get_by_role("link", name="Inquiry").click()
#         page1 = page1_info.value

#         frame = page1.frame_locator('iframe[title="Application"]')

#         frame.get_by_role("textbox", name="Policy Number").fill("00000402000072883")   #"00000402000072199"  402000068350  402000072659
#         page1.keyboard.press("Enter")

#         page1.wait_for_timeout(3000)
#         # ---- Press F8 globally ----
#         page1.keyboard.press("F8")
#         page1.wait_for_timeout(3000)

#         # ==== Posting Data ====
#         scroll_and_click_tree_cell(page1, frame, "Posting Data")
#         page1.wait_for_timeout(2000)

#         # --- Settlement To Date ---
#         frame.locator('input[title="Settlement To"]').fill("31.12.2029")

#         dropdown_btn = frame.locator("[id='M0:46:2:1:2B256:1::3:17-btn']")
#         dropdown_btn.click()
#         frame.get_by_role("option", name="All", exact=True).click()
#         page.wait_for_timeout(1000)

#         refresh = frame.locator('[id="M0:46:2:1:2B256:1::3:76"]')
#         refresh.click()
#         page.wait_for_timeout(1000)

#         # --- Sort of Application ----
#         frame.get_by_text("Application Number").nth(2).click()
#         frame.get_by_label("Document header").get_by_role("button", name="Sort in Ascending Order").click()
#         page.wait_for_timeout(1000)


#         current_app = ""
#         contract_total = 0.0
#         stamp_total = 0.0

#         total_rows = frame.locator("span[id^='grid#'][id$=',5#if']").count()

#         for row in range(1, total_rows + 1):

#             # ---------------- Application Number ----------------
#             app_locator = frame.locator(f"span[id$='#{row},1#if']")

#             if app_locator.count():
#                 app = app_locator.inner_text().strip()

#                 if app:
#                     # If another application is found, stop processing
#                     if current_app:
#                         break

#                     current_app = app
#                     print(f"\nApplication Number : {current_app}")

#             # ---------------- Amount ----------------
#             amount = frame.locator(f"span[id$='#{row},5#if']").inner_text().strip()
#             amount_value = float(amount.replace(",", "").replace("-", ""))

#             # ---------------- Icon ----------------
#             icon = frame.locator(f"svg[id$='#{row},3#icp'] use").get_attribute("xlink:href")

#             # ---------------- Stamp Duty ----------------
#             if amount_value == 10:
#                 stamp_total += amount_value
#                 print("\nStamp Duty             :", amount)

#             # ---------------- ACT Premium ----------------
#             elif icon.endswith("s_s_ledi"):
#                 print("ACT Premium            :", amount)

#             # ---------------- Contract Premium ----------------
#             elif icon.endswith("s_s_ledg"):

#                 contract_total += amount_value
#                 print("\nContract Premium       :", amount)

#                 # Double click the Contract Premium
#                 amount_cell = frame.locator(f"span[id$='#{row},5#if']")
#                 amount_cell.dblclick()

#                 page.wait_for_timeout(2000)

#                 # ------------- GROSS & SST ------
#                 gross = frame.locator('[id*="C263#1,4#if"]').first.inner_text().strip()
#                 sst = frame.locator('[id*="C263#2,4#if"]').first.inner_text().strip()

#                 gross_amt = float(gross.replace(",", "").replace("-", ""))
#                 sst_amt = float(sst.replace(",", "").replace("-", ""))

#                 expected = round(gross_amt + sst_amt, 2)
#                 if expected == amount_value:
#                     print("Premium Matched")
#                 else:
#                     print(f"Premium Mismatch - Expected: {expected:.2f}, Actual: {amount_value:.2f}")

#         # ---------------- Totals ----------------
#         print(f"\nTotal Contract Premium : {contract_total:.2f}")
#         print(f"Total Stamp Duty       : {stamp_total:.2f}")
#         print(f"Overall Premium        : {contract_total + stamp_total:.2f}")

#     finally:
#         pm_logout(page1)

# @pytest.mark.no_network_logger
# def test_nb(page):
#     # first_login(page)
#     # second_login(page)
#     try:
#         page.goto("https://tus4appuat.tuneprotect.com:44303/sap/bc/ui2/flp#ZPM_SEM_OBJ-display")
#         # page.goto("https://tus4appdev.tuneprotect.com:44300/sap/bc/ui2/flp#ZPM_SEM_OBJ-display")
#         # page.wait_for_load_state("networkidle")
#         # page.get_by_role("textbox", name="User").click()
#         # page.get_by_role("textbox", name="User").fill("SSANTHOSH")
#         # page.get_by_role("textbox", name="Password").click()
#         # page.get_by_role("textbox", name="Password").fill("Quality@12345")
#         # page.get_by_role("button", name="Log On").click()

#         page.get_by_label("User").fill("VARAVINDH")
#         page.get_by_label("Password").fill("Serole@2233")
#         page.get_by_role("button", name="Log On").click()
#         page.wait_for_load_state("networkidle")

#         frame = page.locator("iframe[title='Application']").content_frame

#         frame.get_by_role("textbox", name="Policy Start Required").click()
#         frame.get_by_role("textbox", name="Policy Start Required").fill("21.07.2026")
#         frame.get_by_role("textbox", name="Submission To PP Date Required").click()
#         frame.get_by_role("textbox", name="Submission To PP Date Required").fill("21.07.2026")
#         frame.get_by_role("textbox", name="Received Date Required").click()
#         frame.get_by_role("textbox", name="Received Date Required").fill("21.07.2026")

#         frame.get_by_role("textbox", name="Sales Prod.Templ.ID Required").click()
#         frame.get_by_role("textbox", name="Sales Prod.Templ.ID Required").fill("MTPLMC000000")
#         page.wait_for_timeout(1000)
#         page.keyboard.press("Enter")

#         frame.get_by_role("textbox", name="Acquisition Type Required").click()
#         frame.get_by_role("option", name="New Business").click()
#         page.keyboard.press("F8")

#         # ---------- Business Partner --------
#         frame.get_by_role("button", name="Detail").click()
#         frame.get_by_role("textbox", name="Business Partner Required").click()
#         frame.get_by_role("textbox", name="Business Partner Required").fill("1000007765")
#         page.keyboard.press("F8")

#         # --------- Commission Contract -------
#         frame.get_by_role("tab", name="Commission").click()
#         page.wait_for_timeout(1000)
#         frame.get_by_role("button", name="Add").click()
#         frame.get_by_role("textbox", name="Comm. Contract No.").click()
#         frame.get_by_role("textbox", name="Comm. Contract No.").fill("2210001267")
#         page.keyboard.press("F8")

#         frame.get_by_role("button", name="Complete Business Transaction").click()

#         page.wait_for_timeout(3000)
#         frame.get_by_text("Motorcycle", exact=True).nth(1).dblclick()
#         frame.get_by_label("Level 2 Expanded").get_by_text("Motorcycle").click()
#         frame.get_by_label("Level 2 Expanded").get_by_text("Motorcycle").dblclick()

#         # --------- Contract Data ---------
#         frame.get_by_role("textbox", name="Coverage Type Required").click()
#         frame.get_by_role("option", name="Comprehensive").click()

#         # --------- RISK Insured Object ---------
#         frame.get_by_role("tab", name="Risk").click()

#         frame.get_by_role("button", name="Detail").click()
#         frame.get_by_role("button", name="Create").click()
#         frame.get_by_role("textbox", name="Vehicle reg. no.").click()
#         frame.get_by_role("textbox", name="Vehicle reg. no.").fill("W4421Q")
#         frame.get_by_role("textbox", name="Vehicle reg. no.").press("Enter")
#         frame.get_by_role("textbox", name="Category").click()
#         page.wait_for_timeout(2000)
#         page.keyboard.press("Control+S")
#         try:
#             frame.get_by_role("button", name="Yes").click(timeout=3000)
#         except:
#             pass
#         frame.get_by_role("button", name="Complete").click()
#         try:
#             frame.get_by_role("button", name="Yes").click(timeout=3000)
#         except:
#             pass

#         frame.get_by_role("textbox", name="Unit Type Required").click()
#         frame.get_by_role("option", name="CC CC").click()
#         page.wait_for_timeout(1000)
#         page.keyboard.press("F8")
#         page.wait_for_timeout(1000)
#         frame.get_by_role("button", name="Complete Business Transaction").click()

#         page.wait_for_timeout(3000)
#         frame.get_by_text("Comprehensive").dblclick()
#         frame.get_by_text("Comprehensive", exact=True).click()
#         page.wait_for_timeout(2000)
#         frame.get_by_text("Comprehensive", exact=True).dblclick()
#         frame.get_by_role("tab", name="Limit/Deductible").click()

#         page.wait_for_timeout(1000)
#         frame.get_by_role("button", name="Complete Business Transaction").click()
#         page.wait_for_timeout(1000)
#         frame.get_by_role("button", name="Save  Emphasized").click()
#         page.wait_for_timeout(1000)
#         frame.get_by_role("button", name="Check").click()
#         page.wait_for_timeout(1000)
#         frame.get_by_role("button", name="Calculate Application").click()
#         page.wait_for_timeout(1000)
#         page.pause()

#     finally:
#         page.locator("#meAreaHeaderButton").click()
#         page.get_by_text("Sign Out").click()
#         page.get_by_role("button", name="OK").click()


from test_pc import  test_pc_motor

@pytest.mark.no_network_logger
def test_demo(page):
    try:
        test_pc_motor(page)
    except:
        pass
    try:
        test_pc_motor(page)
    except:
        pass
    try:
        test_pc_motor(page)
    except:
        pass