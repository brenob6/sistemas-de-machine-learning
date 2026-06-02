from abc import ABC, abstractmethod
from playwright.sync_api import Download, Route, Request
import logging
import os


class Scraper(ABC):
    def __init__(self, url: str):
        self.url = url

    @abstractmethod
    def scrap(self, date: str | None = None) -> list[str] | None:
        raise NotImplementedError

    def on_download(self, download: Download) -> str:
        DOWNLOAD_PATH = "process/"
        os.makedirs(DOWNLOAD_PATH, exist_ok=True)
        file_path = f"{DOWNLOAD_PATH}{download.suggested_filename}"
        logging.info(f"Download started: {download.url}")
        download.save_as(file_path)
        logging.info(f"Download completed: {file_path}")
        return file_path

    def block_resources(self, route: Route, request: Request):
        blocked_types = ["image", "stylesheet", "font", "media", "websocket"]
        if request.resource_type in blocked_types:
            route.abort()
        else:
            route.continue_()
