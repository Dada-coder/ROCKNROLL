from playwright.sync_api import Page, Playwright, sync_playwright, expect

def test_pw_inspector_code(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://demoqa.com/")
    page.locator("div").filter(has_text="Elements").nth(5).click()
    page.get_by_role("listitem").filter(has_text="Text Box").click()
    page.get_by_role("textbox", name="Full Name").click()
    page.get_by_role("textbox", name="Full Name").fill("da pizda da")
    page.pause()
    page.get_by_role("textbox", name="name@example.com").click()
    page.get_by_role("textbox", name="name@example.com").fill("asdgfasg@mail.ru")
    page.get_by_role("textbox", name="Current Address").click()
    page.get_by_role("textbox", name="Current Address").fill("adress 228")
    page.locator("#permanentAddress").click()
    page.locator("#permanentAddress").fill("1337 uk rf")
    page.get_by_role("button", name="Submit").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    test_pw_inspector_code(playwright)


