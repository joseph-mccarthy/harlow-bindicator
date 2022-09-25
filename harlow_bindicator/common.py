def common_setup():
    import argparse
    import logging

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

    return args