iimport sqlite3
from nba_api.stats.endpoints import teamyearbyyearstats

# Connect to the SQLite database
conn = sqlite3.connect('nba_stats.db')
cur = conn.cursor()

# Define the team IDs and names for the seven teams of interest
teams_data = {
    1610612759: "San Antonio Spurs",
    1610612752: "New York Knicks",
    1610612744: "Golden State Warriors",
    1610612737: "Atlanta Hawks",
    1610612738: "Boston Celtics",
    1610612747: "Los Angeles Lakers",
    1610612739: "Cleveland Cavaliers",
}

# Function to fetch and insert team statistics into the database
def fetch_and_insert_team_stats(team_id, team_name):
    team_stats = teamyearbyyearstats.TeamYearByYearStats(team_id=team_id)
    team_stats_df = team_stats.get_data_frames()[0]
    team_stats_df['Year'] = team_stats_df['YEAR'].str[:4].astype(int)
    team_stats_df = team_stats_df[team_stats_df['Year'] >= 1979]

    for index, row in team_stats_df.iterrows():
        cur.execute('''INSERT INTO team_stats (team_id, team_name, year, three_point_attempts, three_point_made, three_point_percentage, po_wins, wins, losses)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (team_id, team_name, row['Year'], row['FG3A'], row['FG3M'], row['FG3_PCT'], row['PO_WINS'], row['WINS'], row['LOSSES']))
    conn.commit()

# Fetch and insert team statistics for each team
for team_id, team_name in teams_data.items():
    fetch_and_insert_team_stats(team_id, team_name)

# Close the database connection
conn.close()




