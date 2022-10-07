def common_setup():
    import argparse
    import logging

    parser = argparse.ArgumentParser(description="Get List of Bin Collections for UPRN")
    parser.add_argument(
        "--uprn", type=int, help="Unique Property Reference Number",
    )
   
    args = parser.parse_args()

    logging.basicConfig(
        level="INFO",
        format="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    if not args.uprn:
        logging.error("exiting no UPRN provided unable to proceed.")
        exit(1)
            

    return args