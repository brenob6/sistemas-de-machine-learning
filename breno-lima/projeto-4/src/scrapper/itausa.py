from playwright.sync_api import Request, Route, sync_playwright

URL = "https://ri.itausa.com.br/informacoes-financeiras/central-de-resultados/"
# URL = "https://sandbox.oxylabs.io/"


def on_download(download, filename):
    print(f"Download started: {filename}")
    download.save_as(filename)
    print(f"Download completed: {filename}")


def block_resources(route: Route, request: Request):
    blocked_types = ["image", "stylesheet", "font", "media", "websocket"]

    if request.resource_type in blocked_types:
        route.abort()
    else:
        route.continue_()


def extract_itausa_data():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        page = browser.new_page()
        page.route("**/*", block_resources)
        page.on(
            "download",
            lambda download: on_download(download, filename="downloaded_file.pdf"),
        )

        page.goto(URL)

        page.wait_for_selector("table")
        table = page.query_selector("table")
        if not table:
            print("Tabela não encontrada.")
            return
        rows = table.query_selector_all("tr")
        report_row = rows[1]

        links = report_row.query_selector_all("a")
        if not links:
            print("Nenhum link encontrado na linha do relatório.")
            return

        for link in links:
            link.click()

        page.wait_for_event("download")

        browser.close()


extract_itausa_data()
