import bs4
from requests_html import HTMLSession
from dataclasses import dataclass
import datetime


@dataclass
class Collection:

    type: str
    date: str

    def __init__(self, type, date) -> None:
        self.type = type
        self.date = date


@dataclass
class CollectionDate:

    date: str
    caddy: Collection
    wheelie: Collection

    def __init__(self, caddy: Collection, wheelie: Collection) -> None:
        self.caddy = caddy
        self.wheelie = wheelie
        self.date = wheelie.date


class Api:

    uprn: int
    url: str = "https://selfserve.harlow.gov.uk/appshost/firmstep/self/apps/custompage/bincollectionsecho?uprn="

    def __init__(self, uprn) -> None:
        self.uprn = uprn

    def get_data(self):
        data_url = f"{self.url}{self.uprn}"
        session = HTMLSession()
        r = session.get(data_url)
        r.html.render(timeout=20)
        session.close()
        soup = bs4.BeautifulSoup(r.html.html, "html.parser")
        collections = soup.find_all(attrs={"class": ["collectionsrow"]})
        collections.pop(0)

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

        return day_data

    def __get_type(self, data):
        return data[0]

    def __get_date(self, data):
        raw_date = data[0].split("- ", 1)[1]
        return datetime.datetime.strptime(raw_date, "%d %b %Y").strftime("%d/%m/%Y")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Get List of Bin Collections for UPRN")
    parser.add_argument(
        "--uprn", type=int, help="Unique Property Reference Number", required=True
    )
    args = parser.parse_args()
    api = Api(args.uprn)
    data = api.get_data()
    for collection in data:
        print(collection)
