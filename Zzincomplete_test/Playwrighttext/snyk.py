from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch()
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://security.snyk.io/vuln")
    page.get_by_role("row", name="M Cross-site Request Forgery (CSRF) modoboa [,2.1.0) pip 23 Apr 2023").get_by_role("link", name="Cross-site Request Forgery (CSRF)").click()
    page.get_by_role("button", name="See more").click()
    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
