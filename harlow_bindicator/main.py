from data import CollectionDate
from api import Api
from common import common_setup
import logging
import json
from datetime import datetime
import paho.mqtt.client as paho


class Bindicator:

    uprn: int
    api: Api

    def __init__(self, uprn: int) -> None:
        self.uprn = uprn
        self.api = Api(uprn)
        logging.info(f"running Bindicator for property {self.uprn}")

    def run(self):

        collections = self.api.get_data()

        if collections:
            next_collection = collections[0]
            is_bin_day = self.__is_today_bin_day(next_collection)
            payload = json.dumps({
                "date": next_collection.date.strftime("%d/%m/%Y"),
                "bin_day": is_bin_day,
                "bin_type": next_collection.wheelie.bin_type
            })
            self.__send_message(payload)

    def __send_message(self, payload):
        broker = "broker"
        topic = "application/bindicator"

        client = paho.Client(client_id="bindicator")
        client.connect(broker)
        client.publish(topic, payload)

    def __is_today_bin_day(self, collection: CollectionDate) -> bool:
        return collection.date.date() == datetime.now().date()


if __name__ == "__main__":
    args = common_setup()
    logging.info("starting Harlow Bindicator")
    bindicator = Bindicator(args.uprn)
    bindicator.run()
