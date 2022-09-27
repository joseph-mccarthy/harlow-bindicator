from twilio.rest import Client
from data import Collection
import os
import logging


class Twilio:

    phone_numbers = []
    client = Client()
    service_id = os.getenv('MESSAGE_SERVICE_SID')

    def __init__(self, numbers) -> None:
        self.phone_numbers = numbers

    def send_notification(self, collection: Collection)-> None:
        for number in self.phone_numbers:
            logging.info(f"sending notification to {number}")
            self.client.messages.create(  
                              messaging_service_sid='MGd0c0fc1bc9c073ace756d6549c2e1b03', 
                              body=f"Take out the {collection.bin_type} today.",      
                              to=number
                          ) 

if __name__ == "__main__":
    import argparse
    
    logging.basicConfig(
        level="INFO",
        format="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    parser = argparse.ArgumentParser(description="Send Test Notification to a list of numbers")
    parser.add_argument('--phone_numbers', type=str, nargs='+')
    args = parser.parse_args()
    twilio = Twilio(args.phone_numbers)
    collection = Collection("Recycling", "22/09/2022")
    twilio.send_notification(collection)