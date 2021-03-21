import requests
from bs4 import BeautifulSoup


if __name__ == '__main__':
    URL = 'https://inara.cz/galaxy-communitygoals/'
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')

    main = soup.find_all(name='div', class_='maincontent1')

    main_blocks = soup.select('.maincontent1 > .mainblock')

    community_goals = []

    for block in main_blocks:
        cg = {}
        cg['title'] = block.find_previous_sibling('h3').text
        infos = block.select('.itempaircontainer')

        # Get the main info
        for pair in infos:
            key = pair.select_one('.itempairlabel').text[:-1]  # remove the ':' at the end
            value = pair.select_one('.itempairvalue').text
            cg[key] = value

        # Get the rewards structure
        tbl = block.find('tbody')
        rows = tbl.find_all('tr')
        cg['Top10'] = rows[0].find_all('td')[1].text[2:]
        cg['Top10pct'] = rows[1].find_all('td')[1].text[2:]
        cg['Top25pct'] = rows[2].find_all('td')[1].text[2:]
        cg['Top50pct'] = rows[3].find_all('td')[1].text[2:]
        cg['Top75pct'] = rows[4].find_all('td')[1].text[2:]
        cg['Top100pct'] = rows[5].find_all('td')[1].text[2:]

        community_goals.append(cg)

    ongoing_cg = [cg for cg in community_goals if cg['Status'] == 'Ongoing']
