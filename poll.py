import argparse
import logging
import scrape
import save
import time
import os

logging.basicConfig(
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%dT%H:%M:%S',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

POLL_DEFAULT = 600
FILE_DEFAULT = 'CG.csv'


def create_argparser():
    new_parser = argparse.ArgumentParser(description='Inara CG Scraper')
    new_parser.add_argument(
        '-t', '--time',
        type=int,
        default=POLL_DEFAULT,
        help=f"Time between polls (seconds). Defaults to {POLL_DEFAULT}.",
    )
    new_parser.add_argument(
        '-f', '--filename',
        type=str,
        default=FILE_DEFAULT,
        help=f"File to save to. Default name is {FILE_DEFAULT}",
    )
    return new_parser


if __name__ == '__main__':
    parser = create_argparser()
    args = parser.parse_args()

    file_path = os.path.abspath(args.filename)

    logger.info(f"Starting poller.")
    logger.info(f"Time between polls: {args.time} seconds")
    logger.info(f"Saving to file: {file_path}")

    while True:
        logger.info("Scraping data...")
        scraped_data = scrape.scrape_inara_cgs()
        ongoing_cgs = [data for data in scraped_data if data['status'] == 'Ongoing']
        logger.info("Saving data...")
        save.save_to_csv(file_path, ongoing_cgs)

        logger.info(f"Complete. Next poll in {args.time} seconds.")

        time.sleep(int(args.time))