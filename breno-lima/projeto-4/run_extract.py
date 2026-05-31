import logging
import os
import sys

from src.extract import table

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)

OUTPUT_DIR = "process"


def run_extract(pdf_path: str):
    if not os.path.exists(pdf_path):
        logger.error(f"Arquivo não encontrado: {pdf_path}")
        sys.exit(1)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    basename = os.path.splitext(os.path.basename(pdf_path))[0]
    output_csv = os.path.join(OUTPUT_DIR, f"{basename}.csv")

    logger.info(f"Extraindo tabelas de: {pdf_path}")
    table.extract_tables_from_pdf(pdf_path, output_csv)
    logger.info(f"CSV gerado em: {output_csv}")


if __name__ == "__main__":
    pdf = sys.argv[1] if len(sys.argv) > 1 else "exemplo_Boletim_Conjuntura_2025_3T.pdf"
    run_extract(pdf)
