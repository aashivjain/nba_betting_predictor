from nba_api.stats.endpoints import leaguegamefinder
#from nba_api.stats.endpoints import boxscoreadvancedv2
from nba_api.stats.static import teams
import pandas as pd
import time
from pathlib import Path

def fetch_all_team_games() -> pd.DataFrame: # function to fetch all games for all NBA teams
    nba_teams = teams.get_teams() # getting all teams into a df
    all_games = []

    for team in nba_teams:
        print(f"Fetching {team['full_name']}...")
        gamefinder = leaguegamefinder.LeagueGameFinder(
            team_id_nullable=team["id"]
        )
        df = gamefinder.get_data_frames()[0]
        df["TEAM_NAME"] = team["full_name"]  # add team name column
        all_games.append(df)

        time.sleep(0.6) # slows down just in case nba api has a rate limit

    combined = pd.concat(all_games, ignore_index=True)
    return combined

if __name__ == "__main__": # adding all the data to raw folder as all_games.csv
    raw_dir = Path(__file__).resolve().parents[2] / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    all_games_df = fetch_all_team_games() # calls basic stats function
    # game_ids = all_games_df["GAME_ID"].unique().tolist() # gets unique game ids
    
    out_file = raw_dir / "all_games.csv"
    all_games_df.to_csv(out_file, index=False) # saves to csv
    print(f"Saved combined data to: {out_file}")