import requests
from bs4 import BeautifulSoup
import logging
from typing import List, Dict
from collections import OrderedDict
from datetime import datetime

import re

logger = logging.getLogger(__file__)

INARA_URL = "https://inara.cz/galaxy-communitygoals/"

date_matcher = re.compile(r'((?P<days>\d+)D)? ?((?P<hours>\d+)H)? ?((?P<mins>\d+)M)?')


def to_int(string):
    """Just replaces the number strings which have commas to an int."""
    return int(string.replace(",", ""))


def scrape_inara_cgs(url: str = INARA_URL) -> List[Dict]:
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")
    main_blocks = soup.select(".maincontent1 > .mainblock")

    community_goals = []

    logger.debug("Parsing blocks.")
    for block in main_blocks:
        cg = OrderedDict()
        cg['title'] = block.find_previous_sibling('h3').text
        cg['timestamp'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        logger.info(f"Starting to parse: {cg['title']}")
        info = block.select('.itempaircontainer')

        # Get the main info
        logger.debug(f"Parsing main info block.")
        for pair in info:
            key_name = pair.select_one('.itempairlabel').text.replace(" ", "_")
            key = key_name.replace(":", "").lower()
            value = pair.select_one(".itempairvalue").text
            cg[key] = value

        logger.debug(f"Cleaning up the main block")
        cg["contributors"] = to_int(cg["contributors"])
        contributions = cg["contributions"].split("/")
        cg["contributions"] = to_int(contributions[0])

        # gets rid of the "percent" bit: like (10%)
        cg["contributions_total"] = to_int(contributions[0].split(" ")[0])

        # Convert the time left:
        logger.debug('Converting time left.')
        if cg["status"] == "Ongoing":
            match = date_matcher.fullmatch(cg['time_left'])
            cg["days_left"] = int(match['days'] or 0)
            cg["hours_left"] = int(match['hours'] or 0)
            cg["minutes_left"] = int(match['mins'] or 0)

        # Get the rewards structure
        logger.debug(f"Parsing rewards structure.")
        tbl = block.find("tbody")
        rows = tbl.find_all("tr")

        items = [
            "top10cmdrs",
            "top10pct",
            "top25pct",
            "top50pct",
            "top75pct",
            "top100pct",
        ]

        for i in range(0, len(items)):
            logger.debug(f'Parsing {rows[i].text}')
            # Split something like: "500 to 1,000" to ["500", "1,000"]
            values = rows[i].find_all("td")[1].text[2:].split(" to ")
            # Now clean that up.
            cg[items[i] + "_min"] = to_int(values[0])
            cg[items[i] + "_max"] = to_int(values[1])

        logger.info(f"Finished parsing {cg['title']}")
        community_goals.append(cg)

    return community_goals

