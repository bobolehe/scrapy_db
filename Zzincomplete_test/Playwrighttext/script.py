

from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch()
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.baidu.com/")
    page.locator("#kw").fill("kk")
    page.get_by_role("button", name="百度一下").click()
    page.wait_for_timeout(5000)
    text = page.content()
    print(text)
    with open('tesstt.html', 'w',encoding='utf-8') as file_read:
        file_read.write(text)
    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)