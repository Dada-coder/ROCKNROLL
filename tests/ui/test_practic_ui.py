from playwright.sync_api import Page
import time


def test_ui_form_add(page: Page):
    page.goto('https://demoqa.com/webtables')
    page.locator('[id="addNewRecordButton"]').click()
    page.locator('[id="registration-form-modal"]').is_visible()
    page.fill('[id="firstName"]', "First")
    page.fill('[id="lastName"]', "First")
    page.fill('[id="userEmail"]', "First@mail.ru")
    page.fill('[id="age"]', "33")
    page.fill('[id="salary"]', "333")
    page.fill('[id="department"]', "First")
    page.locator('[id="submit"]').click()




    time.sleep(3)

def test_demoqa_forms(page: Page):
    page.goto('https://demoqa.com/automation-practice-form')
    page.fill('#firstName', "First")
    page.type('#lastName', "Second")
    page.fill('#userEmail', "First@mail.ru")
    page.check('[id="gender-radio-2"]')

