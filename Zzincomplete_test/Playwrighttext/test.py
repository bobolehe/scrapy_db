import time

from playwright.sync_api import Playwright, sync_playwright, expect
import re

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://security.snyk.io/vuln/SNYK-RUBY-URI-5291533")
    page.get_by_role("button", name="See more").click()
    buttons = page.query_selector_all("div[aria-label='Expand this section']")
    for button in buttons:
        print(button)

    # page.locator("div").filter(has_text=re.compile(r"^Expand this section NVD$")).locator("svg").click()
    # page.locator("div").filter(has_text=re.compile(r"^Expand this section Red Hat$")).locator("svg").click()


with sync_playwright() as playwright:
    run(playwright)
