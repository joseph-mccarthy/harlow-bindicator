from dataclasses import dataclass
from datetime import datetime

@dataclass
class Collection:

    bin_type: str
    date: datetime

    def __init__(self, type, date) -> None:
        self.bin_type = type
        self.date = datetime.strptime(date, "%d/%m/%Y")


@dataclass
class CollectionDate:

    date: datetime
    caddy: Collection
    wheelie: Collection

    def __init__(self, caddy: Collection, wheelie: Collection) -> None:
        self.caddy = caddy
        self.wheelie = wheelie
        self.date = wheelie.date

