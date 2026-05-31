from playwright.sync_api import Download, Request, Route, sync_playwright
import logging
import os

logging.basicConfig(level=logging.INFO)

URL = "https://ri.itausa.com.br/informacoes-financeiras/central-de-resultados/"
# URL = "https://sandbox.oxylabs.io/"


def on_download(download: Download) -> str:
    DOWNLOAD_PATH = "process/"
    os.makedirs(DOWNLOAD_PATH, exist_ok=True)
    file_path = f"{DOWNLOAD_PATH}{download.suggested_filename}"
    logging.info(f"Download started: {download.url}")
    download.save_as(file_path)
    logging.info(f"Download completed: {file_path}")
    return file_path


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
            lambda _: None,  # tratado manualmente no loop
        )

        page.goto(URL)

        page.wait_for_selector("table")
        table = page.query_selector("table")
        if not table:
            logging.info("Tabela não encontrada.")
            return
        rows = table.query_selector_all("tr")
        report_row = rows[1]

        links = report_row.query_selector_all("a")
        if not links:
            logging.info("Nenhum link encontrado na linha do relatório.")
            return
        logging.info(f"{len(links)} link(s) encontrado(s) na linha do relatório.")

        downloaded_files: list[str] = []
        for link in links:
            link.click()
            download_event = page.wait_for_event("download")
            file_path = on_download(download_event)
            downloaded_files.append(file_path)

        page.close()
        browser.close()
        return downloaded_files
