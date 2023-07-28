import sqlite3
import json

# Connect to the SQLite database
conn = sqlite3.connect('nba_stats.db')
cur = conn.cursor()

# Fetch the team statistics from the database
cur.execute('''SELECT * FROM team_stats ORDER BY team_id, year''')
team_stats = cur.fetchall()

# Close the database connection
conn.close()

# Group the team statistics by team ID
team_data = {}
for row in team_stats:
    team_id, year, three_point_attempts, three_point_made, three_point_percentage, po_wins, wins, losses = row
    if team_id not in team_data:
        team_data[team_id] = {
            'team_id': team_id,
            'team_data': []
        }
    team_data[team_id]['team_data'].append({
        'year': year,
        'three_point_attempts': three_point_attempts,
        'three_point_made': three_point_made,
        'three_point_percentage': three_point_percentage,
        'po_wins': po_wins,
        'wins': wins,
        'losses': losses
    })

# Convert the team_data dictionary to a list and sort by team ID
team_data_list = sorted(list(team_data.values()), key=lambda x: x['team_id'])

# Save the data as JSON to a file
with open('data.json', 'w') as json_file:
    json.dump(team_data_list, json_file, indent=4)
