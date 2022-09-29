def common_setup():
    import argparse
    import logging
    import os

    parser = argparse.ArgumentParser(description="Get List of Bin Collections for UPRN")
    parser.add_argument(
        "--uprn", type=int, help="Unique Property Reference Number",
    )
    parser.add_argument(
        "--log", type=str, required=False, help="Log Level", default=logging.INFO
    )

    parser.add_argument('--phone_numbers', type=str, nargs='+')
    
    args = parser.parse_args()

    logging.basicConfig(
        level=args.log,
        format="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    if not args.uprn:
        logging.warn("No UPRN provided checking system variables.")
        args.uprn = os.getenv('UPRN')
        if not args.uprn:
            logging.error("Exiting no UPRN provided unable to proceed.")
            exit(1)

    return args