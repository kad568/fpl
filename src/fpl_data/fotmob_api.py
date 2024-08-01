import requests
from  bs4 import BeautifulSoup as bs
import chompjs
from pathlib import Path
import json
import time

FOTMOB_BASE_URL = "https://www.fotmob.com"
SCRIPT_PATH = Path(__file__).parent.resolve()

def get_prem_team_data_links_203_2024():

    url = f"{FOTMOB_BASE_URL}/leagues/47/stats/premier-league/teams?season=2023-2024"

    response = requests.get(url)
    soup = bs(response.text, "html.parser")
    scripts = soup.find_all('script')

    script_with_data = scripts[-1]

    javascript_soup = bs(str(script_with_data), "html.parser")

    script_tag = javascript_soup.find("script")

    json_data = script_tag.string

    json_data = json.loads(json_data)["props"]["pageProps"]["stats"]["teams"]

    team_links = [x["fetchAllUrl"] for x in json_data]
    return json_data


def get_team_link_data(team_link):

    response = requests.get(team_link)
    json_data = json.loads(response.text)


    json_data = {x["TeamId"]: x["StatValue"] for x in json_data["TopLists"][0]["StatList"]}

    return json_data


def main():

    # data = get_prem_team_data_203_2024()

    # with open(str(SCRIPT_PATH / "fotmob_pl_team_2023_2024.json"), "w") as file:
    #     json.dump(data, file, indent=4)

    with open(str(SCRIPT_PATH / "fotmob_pl_team_2023_2024.json"), "r") as file:
        team_json = json.load(file)
    
    team_links = [x["fetchAllUrl"] for x in team_json]

    # with open(str(SCRIPT_PATH / "fotmob_pl_team_data_links_2023_2024.txt"), "w") as file:
        
    #     for link in team_links:
    #         file.writelines(f"{link}\n")

    data = get_team_link_data(team_links[0])

    with open(str(SCRIPT_PATH / "example_team_data.json"), "w") as file:
        json.dump(data, file, indent=4)

    
    


    



if __name__ == "__main__":

    main()