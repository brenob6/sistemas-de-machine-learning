import logging
import os
import re

import pymupdf4llm

from scrapper.factory import ScraperFactory
from signature import hash
from signature.registry import registry

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


def pipeline(company: str = "itausa", date: str | None = None):
    logger.info("Iniciando pipeline")
    scraper = ScraperFactory.create(company)
    downloaded_files = scraper.scrap(date=date)
    if not downloaded_files:
        logger.warning("Nenhum arquivo baixado")
        return

    logger.info(f"{len(downloaded_files)} arquivo(s) baixado(s)")

    for file in downloaded_files:
        file_hash = hash.get_file_hash(file)

        if registry.is_already_processed(file_hash):
            logger.info(f"[skip] {file} já processado (hash: {file_hash[:8]}...)")
            continue

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

    logger.info("Pipeline concluído")
