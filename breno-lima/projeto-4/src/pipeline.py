import logging
import os

from src.scrapper import itausa
from src.signature import hash
from src.signature.registry import registry
from src.extract import table

logger = logging.getLogger(__name__)

OUTPUT_DIR = "process"


def pipeline():
    logger.info("Iniciando pipeline")
    downloaded_files = itausa.extract_itausa_data()
    if not downloaded_files:
        logger.warning("Nenhum arquivo baixado")
        return

    logger.info(f"{len(downloaded_files)} arquivo(s) baixado(s)")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for file in downloaded_files:
        file_hash = hash.get_file_hash(file)

        if registry.is_already_processed(file_hash):
            logger.info(f"[skip] {file} já processado (hash: {file_hash[:8]}...)")
            continue

        logger.info(f"[process] {file} (hash: {file_hash[:8]}...)")
        basename = os.path.splitext(os.path.basename(file))[0]
        output_csv = os.path.join(OUTPUT_DIR, f"{basename}.csv")
        table.extract_tables_from_pdf(file, output_csv)
        logger.info(f"Tabelas extraídas para {output_csv}")

        registry.mark_as_processed(file_hash, {"file": file, "output": output_csv})
        registry.save_registry()

    logger.info("Pipeline concluído")
