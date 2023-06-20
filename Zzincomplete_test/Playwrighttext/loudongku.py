import time

from playwright.sync_api import Playwright, sync_playwright


def main():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=False,
            proxy={
                "server": "http://115.29.177.102:8080"
            }
                                             )
        context = browser.new_context(
            proxy={
                "server": "http://115.29.177.102:8080"
            }
        )
        page = context.new_page()
        page.goto("https://www.cnvd.org.cn/")
        time.sleep(20)
        page.wait_for_selector("#key", state='visible')
        page.fill("#key", "漏洞")
        page.click("text=搜索")
        page.wait_for_selector("#pcontent", state='visible')
        content = page.inner_html("#pcontent")
        print(content)
        browser.close()


if __name__ == "__main__":
    main()
