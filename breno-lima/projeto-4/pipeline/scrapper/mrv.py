import logging
from playwright.sync_api import sync_playwright
from scrapper.scrapper import Scraper

URL = "https://ri.mrv.com.br/informacoes-financeiras/central-de-resultados/"


class MRVScraper(Scraper):
    def __init__(self):
        super().__init__(URL)

    def scrap(self, date: str | None = None) -> list[str] | None:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.route("**/*", self.block_resources)
            page.on("download", lambda _: None)

            page.goto(self.url)

            if date:
                pass

            page.wait_for_selector("table")
            table = page.query_selector("table")
            if not table:
                logging.info("Tabela não encontrada.")
                return None

            row = table.query_selector("tr:nth-child(2)")
            if not row:
                logging.info("Linha do relatório não encontrada.")
                return None

            links = row.query_selector_all("a")
            if not links:
                logging.info("Nenhum link encontrado na linha do relatório.")
                return None

            logging.info(f"{len(links)} link(s) encontrado(s) na linha do relatório.")
            downloaded_files: list[str] = []

            for link in links:
                with page.expect_download() as download_info:
                    link.click()
                file_path = self.on_download(download_info.value)
                downloaded_files.append(file_path)

            page.close()
            browser.close()
            return downloaded_files
