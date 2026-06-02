import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from pipeline import pipeline

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)

scheduler = BlockingScheduler()


@scheduler.scheduled_job("cron", day_of_week="mon", hour=0, minute=0)
def run():
    pipeline()


if __name__ == "__main__":
    run()
    scheduler.start()
