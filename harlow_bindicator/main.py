from api import Api, Collection
from common import common_setup
import logging
import pause
from datetime import datetime
from datetime import timedelta
from gpiozero import LED


class Bindicator:

    uprn: int
    api: Api
    bin_type: str
    bin_day: bool = False

    bin_day_led = LED(2)
    recycling_bin_led = LED(3)
    rubbish_bin_led = LED(4)
    active_led = LED(26)

    def __init__(self, uprn: int) -> None:
        self.uprn = uprn
        self.api = Api(uprn)
        logging.info(f"running Bindicator for property {self.uprn}")

    def run(self):
        self.active_led.blink()
        while True:
            collections = self.api.get_data()

            if collections:
                collection = collections[0]
                if self.__is_today_bin_day(collection):
                    self.__configure_for_bin_day(collection)
                    logging.info(f"today is bin day for {self.bin_type}")
                else:
                    if self.bin_day:
                        logging.info(f"today {datetime.now().date()} is not bin day")
                    self.__turn_lights_off()
                    self.bin_day = False
            else:
                pause.minutes(30)
                continue  
          
            tomorrow = (datetime.now() + timedelta(days=1)).replace(
                hour=0, minute=1, second=0, microsecond=0
            )
            logging.info(f"waiting till {tomorrow} to run again")
            pause.until(tomorrow)

    def __is_today_bin_day(self, collection: Collection) -> bool:
        return collection.date.date() == datetime.now().date()

    def __turn_lights_off(self):
        self.bin_day_led.off()
        self.recycling_bin_led.off()
        self.rubbish_bin_led.off()

    def __configure_for_bin_day(self, collection: Collection):
        self.bin_day_led.on()
        self.bin_day = True
        self.bin_type = collection.wheelie.bin_type
        self.__turn_on_bin_light(collection)

    def __turn_on_bin_light(self, collection: Collection):
        if collection.wheelie.bin_type == "Recycing":
            self.recycling_bin_led.on()
        else:
            self.rubbish_bin_led.on()


if __name__ == "__main__":
    args = common_setup()
    logging.info("starting Harlow Bindicator")
    bindicator = Bindicator(args.uprn)
    bindicator.run()