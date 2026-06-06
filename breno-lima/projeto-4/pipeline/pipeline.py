from functools import reduce
import logging
import os
import re

import pymupdf4llm

from contracts.contract import ItausaContract
from scrapper.factory import ScraperFactory
from signature import hash
from signature.registry import registry
from model.gemini import geminiModel

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

    try:
        ItausaContract.model_validate_json(structured_data)
        with open(file.replace(".md", ".json"), "w", encoding="utf-8") as f:
            f.write(structured_data)
    except Exception as e:
        logger.error(f"Validation error for {file}: {e}")
        with open(file.replace(".md", ".error.json"), "w", encoding="utf-8") as f:
            f.write(structured_data)


def pdf_to_markdown(file: str, company: str) -> str | None:
    file_hash = hash.get_file_hash(file)

    if registry.is_already_processed(file_hash):
        logger.info(f"[skip] {file} já processado (hash: {file_hash[:8]}...)")
        return

    period = parse_period_from_filename(os.path.basename(file))
    if period:
        quarter, year = period
        output_dir = os.path.join(OUTPUT_DIR, company, str(year))
        output_md = os.path.join(output_dir, f"Q{quarter}.md")
    else:
        output_dir = os.path.join(OUTPUT_DIR, company)
        basename = os.path.splitext(os.path.basename(file))[0]
        output_md = os.path.join(output_dir, f"{basename}.md")

    os.makedirs(output_dir, exist_ok=True)

    logger.info(f"[process] {file} → {output_md} (hash: {file_hash[:8]}...)")
    md_text = pymupdf4llm.to_markdown(doc=file)

    if isinstance(md_text, str):
        open(output_md, "w", encoding="utf-8").write(md_text)

    registry.mark_as_processed(file_hash, {"file": file, "output": output_md})
    registry.save_registry()
    return output_md


def pipeline(company: str = "itausa", date: str | None = None):
    logger.info("Iniciando pipeline")
    scraper = ScraperFactory.create(company)
    downloaded_files = scraper.scrap(date=date)
    if not downloaded_files:
        logger.warning("Nenhum arquivo baixado")
        return

    logger.info(f"{len(downloaded_files)} arquivo(s) baixado(s)")

    for file in downloaded_files:
        markdown_file = pdf_to_markdown(file, company)
        if markdown_file:
            process_markdown(markdown_file)

    logger.info("Pipeline concluído")
