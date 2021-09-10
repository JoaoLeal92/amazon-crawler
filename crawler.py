from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Crawler:
    def __init__(self, driver_path: str) -> None:
        self.DRIVER_PATH: str = driver_path
        self.driver_options: Options = Options()
        self.driver: webdriver.Chrome = None

    def set_driver_options(self, opts: List[str]):
        for opt in opts:
            self.driver_options.add_argument(opt)

    def start_crawler(self, implicit_wait_time: int):
        self.driver = self._start_driver()
        self._set_driver_implicit_wait(implicit_wait_time)
        self._maximize_driver_window()

    def _start_driver(self) -> webdriver.Chrome:
        return webdriver.Chrome(executable_path=self.DRIVER_PATH, options=self.driver_options)

    def _set_driver_implicit_wait(self, wait_time: int):
        self.driver.implicitly_wait(wait_time)

    def _maximize_driver_window(self):
        self.driver.maximize_window()

    def navigate_to_url(self, url: str):
        self.driver.get(url)

    def quit(self):
        self.driver.quit()
