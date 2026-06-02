from playwright.sync_api import sync_playwright
import logging

from scrapper.scrapper import Scraper

URL = "https://ri.itausa.com.br/informacoes-financeiras/central-de-resultados/"


class ItausaScraper(Scraper):
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
                logging.info(f"Filtrando por data: {date}")
                page.wait_for_selector("select#fano")
                select_filter = page.query_selector("select#fano")
                if not select_filter:
                    logging.info("Filtro de data não encontrado.")
                    return None

                page.wait_for_selector("table")
                old_content = page.inner_text("table")

                select_filter.select_option(label=date)

                page.wait_for_function(
                    "(oldContent) => document.querySelector('table')?.innerText !== oldContent",
                    arg=old_content,
                    timeout=10000,
                )

            page.wait_for_selector("table")
            table = page.query_selector("table")
            if not table:
                logging.info("Tabela não encontrada.")
                return None

            rows = table.query_selector_all("tr")
            report_row = rows[1]

            links = report_row.query_selector_all("a")
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


# convenience function mantida para compatibilidade com pipeline.py
def extract_itausa_data(date: str | None = None) -> list[str] | None:
    return ItausaScraper().scrap(date=date)
