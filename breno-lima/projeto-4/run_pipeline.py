import argparse
import logging

from src.pipeline import pipeline

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Executa o pipeline de extração")
    parser.add_argument(
        "--company",
        type=str,
        default="itausa",
        help="Nome da empresa (ex: itausa)",
    )
    parser.add_argument(
        "--date",
        type=str,
        default=None,
        help="Filtro de ano (ex: 2025, 2026)",
    )
    args = parser.parse_args()
    pipeline(company=args.company, date=args.date)
