import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from contracts.contract import ItausaContract
from contracts.mrv import MRVContract
from pipeline import Pipeline
from scrapper.factory import ScraperFactory

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)

scheduler = BlockingScheduler()


@scheduler.scheduled_job("cron", day_of_week="mon", hour=0, minute=0)
def run():
    itausa_scraper = ScraperFactory.create("itausa")
    if not itausa_scraper:
        logging.error("Erro ao criar scraper para Itausa.")
        return

    mrv_scraper = ScraperFactory.create("mrv")
    if not mrv_scraper:
        logging.error("Erro ao criar scraper para MRV.")
        return

    # Pipeline(company="itausa", scraper=itausa_scraper, contract=ItausaContract()).run()
    Pipeline(company="mrv", scraper=mrv_scraper, contract=MRVContract).run()


if __name__ == "__main__":
    # run()
    scheduler.start()
