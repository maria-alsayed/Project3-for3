import sqlite3
from nba_api.stats.endpoints import teamyearbyyearstats

# Connect to the SQLite database
conn = sqlite3.connect('nba_stats.db')
cur = conn.cursor()

# Define the team IDs for the seven teams of interest
team_ids = [1610612759, 1610612752, 1610612744, 1610612737, 1610612738, 1610612747, 1610612739]

# Function to fetch and insert team statistics into the database
def fetch_and_insert_team_stats(team_id):
    team_stats = teamyearbyyearstats.TeamYearByYearStats(team_id=team_id)
    team_stats_df = team_stats.get_data_frames()[0]
    team_stats_df['Year'] = team_stats_df['YEAR'].str[:4].astype(int)
    team_stats_df = team_stats_df[team_stats_df['Year'] >= 1979]

    for index, row in team_stats_df.iterrows():
        cur.execute('''INSERT INTO team_stats (team_id, year, three_point_attempts, three_point_made, three_point_percentage, po_wins, wins, losses)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
            (team_id, row['Year'], row['FG3A'], row['FG3M'], row['FG3_PCT'], row['PO_WINS'], row['WINS'], row['LOSSES']))
    conn.commit()

# Fetch and insert team statistics for each team
for team_id in team_ids:
    fetch_and_insert_team_stats(team_id)

# Close the database connection
conn.close()
