import bs4
from dataclasses import dataclass
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import logging
import time
from data import CollectionDate, Collection
class Api:

    uprn: int
    url: str = "https://selfserve.harlow.gov.uk/appshost/firmstep/self/apps/custompage/bincollectionsecho?uprn="

    def __init__(self, uprn) -> None:
        self.uprn = uprn
        logging.info("starting Bindicator API")

    def get_data(self):
        data_url = f"{self.url}{self.uprn}"

        chrome_options = Options()
        options = [
            "--headless",
            "--disable-gpu",
            "--window-size=1920,1200",
            "--ignore-certificate-errors",
            "--disable-extensions",
            "--no-sandbox",
            "--disable-dev-shm-usage",
        ]
        for option in options:
            chrome_options.add_argument(option)

        executable_path = "/usr/bin/chromedriver"
        chrome_service = Service(executable_path)

        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        logging.info("rendering webpage for collection data")
        start = time.time()
        driver.get(data_url)
        end = time.time()
        logging.info(
            f"render and data collection took {round(((end-start) * 10**3)/1000,2)} seconds"
        )

        soup = bs4.BeautifulSoup(driver.page_source, "html.parser")
        collections = soup.find_all(attrs={"class": ["collectionsrow"]})
        collections.pop(0)

        if collections:
            logging.info(f"loaded bin collection data for {self.uprn}")

        collection_data = []
        for collection in collections:
            children = collection.findChildren("div", recursive=False)
            children.pop(0)
            bin_type = self.__get_type(children[0].contents)
            bin_date = self.__get_date(children[1].contents)
            collection_data.append(Collection(bin_type, bin_date))

        filtered = x = [
            collection_data[i : i + 2] for i in range(0, len(collection_data), 2)
        ]

        day_data = []

        for data in filtered:
            day_data.append(CollectionDate(data[0], data[1]))

        logging.info(f"{len(day_data)} bin collections found")

        return day_data

    def __get_type(self, data):
        return data[0]

    def __get_date(self, data):
        raw_date = data[0].split("- ", 1)[1]
        return datetime.strptime(raw_date, "%d %b %Y").strftime("%d/%m/%Y")


if __name__ == "__main__":
    from common import common_setup

    args = common_setup()
    api = Api(args.uprn)
    data = api.get_data()
    for collection in data:
        print(collection)
