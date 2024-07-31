import json
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns

PATH_TO_HERE = Path(__file__).parent.resolve()

def get_team_fpl_team_data():
    path_to_fpl_json = PATH_TO_HERE / "../fpl_data/fpl_data.json"
    
    with open(path_to_fpl_json, "r") as file:
        fpl_json = json.load(file)

    team_data = fpl_json["teams"]

    team_data = pd.DataFrame(team_data)

    return team_data

def fpl_team_defensive_rating():

    team_data = get_team_fpl_team_data()

    team_data = team_data[["code", "name", "strength", 'strength_overall_home', 'strength_overall_away',
       'strength_attack_home', 'strength_attack_away', 'strength_defence_home',
       'strength_defence_away']] 
    
    # normalize values
    colomns_to_normalize = ['strength_overall_home', 'strength_overall_away',
       'strength_attack_home', 'strength_attack_away', 'strength_defence_home',
       'strength_defence_away']
    
    for col in colomns_to_normalize:
        col_data = team_data[col]
        col_data_normalised = ( col_data - 1040 ) / ( 1370 - 1040 )
        team_data[col] = col_data_normalised

    # sort by average rnk
    row_avg = team_data[['strength_overall_home', 'strength_overall_away']].mean(axis=1)
    row_order = row_avg.sort_values(ascending=False).index
    team_data = team_data.loc[row_order]
    team_data.set_index("name", inplace=True)


    # plot data
    sns.heatmap(team_data[['strength_overall_home', 'strength_overall_away',
       'strength_attack_home', 'strength_attack_away', 'strength_defence_home',
       'strength_defence_away']], annot=True)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


def main():

    fpl_team_defensive_rating()



if __name__ == "__main__":

    main()