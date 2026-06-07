from functools import reduce
import logging
import re
import db

import pymupdf4llm

from contracts.contract import ItausaContract
from scrapper.factory import ScraperFactory
from signature import hash
from model.gemini import geminiModel
from storage.storage import storage

logger = logging.getLogger(__name__)

OUTPUT_DIR = "process"


def parse_period_from_filename(filename: str) -> tuple[int, int] | None:
    """Extract (quarter, year) from filenames like 'Relatório da Administração 1T26.pdf'"""
    match = re.search(r"(\d)T(\d{2})", filename)
    if match:
        quarter = int(match.group(1))
        year = 2000 + int(match.group(2))
        return quarter, year
    return None


def extract_tables_from_markdown(md_text: str) -> str:
    """Extract markdown tables from the text"""
    tables = re.findall(r"(\|.*\|(?:\n\|[-: ]+\|)+\n(?:\|.*\|\n)*)", md_text)

    return reduce(lambda acc, table: acc + f"\n{table}\n", tables, "")


def process_markdown(file: str):
    md_text = open(file, "r", encoding="utf-8").read()
    table = extract_tables_from_markdown(md_text)

    logger.info(f"Processing table from {file}:\n{table}\n")
    structured_data = geminiModel.prompt(table)
    logger.info(f"Structured data:\n{structured_data}\n")

    if not structured_data:
        logger.warning(f"No structured data extracted from {file}")
        return


class Pipeline:
    def run(self):
        downloaded_files = self.scrap()
        if not downloaded_files:
            logger.info("Nenhum arquivo baixado")
            return
        for file in downloaded_files:
            self.Process(file).run()

    def scrap(self, company: str = "itausa", date: str | None = None):
        logger.info("Iniciando pipeline")
        scraper = ScraperFactory.create(company)
        return scraper.scrap(date=date)

    class Process:
        def __init__(self, filepath: str):
            self.filepath = filepath
            self.file_hash = hash.get_file_hash(filepath)
            self.file_content = None

        def run(self):
            if db.exists(sha256=self.file_hash):
                logger.info(f"Arquivo {self.filepath} já processado, pulando.")
                return
            self.to_markdown()
            self.extract_json()

        def to_markdown(self):
            md_text = pymupdf4llm.to_markdown(doc=self.filepath)
            if isinstance(md_text, str):
                storage.upload_processed(md_text)
                self.file_content = md_text

        def extract_json(self):
            if not self.file_content:
                logger.warning(f"No markdown content to process for {self.filepath}")
                return

            table = extract_tables_from_markdown(self.file_content)
            logger.info(f"Processing table from {self.filepath}:\n{table}\n")

            structured_data = geminiModel.prompt(table)
            logger.info(f"Structured data:\n{structured_data}\n")
            if not structured_data:
                logger.warning(f"No structured data extracted from {self.filepath}")
                return

            try:
                ItausaContract.model_validate_json(structured_data)
                # storage.upload_extracted(structured_data, self.file_hash)
                db.save_document(
                    sha256=self.file_hash,
                    company="itausa",
                    document_type="administrative_report",
                    content=structured_data,
                    is_valid=True,
                )

            except Exception:
                # storage.upload_extracted(structured_data, self.file_hash)
                db.save_document(
                    sha256=self.file_hash,
                    company="itausa",
                    document_type="administrative_report",
                    content=structured_data,
                    is_valid=False,
                )
