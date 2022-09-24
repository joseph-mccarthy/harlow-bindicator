from api import Api
import logging


class Bindicator:

    uprn: int
    api: Api

    def __init__(self, uprn: int) -> None:
        self.uprn = uprn
        self.api = Api(uprn)
        logging.info(f"Running Bindicator for Property {self.uprn}")

    def run(self):
        self.api.get_data()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Get List of Bin Collections for UPRN")
    parser.add_argument(
        "--uprn", type=int, help="Unique Property Reference Number", required=True
    )
    parser.add_argument(
        "--log", type=str, required=False, help="Log Level", default=logging.INFO
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=args.log,
        format="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    logging.info("Starting Harlow Bindicator")
    bindicator = Bindicator(args.uprn)
    bindicator.run()
