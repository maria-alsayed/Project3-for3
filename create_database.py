import sqlite3

# Connect to or create the SQLite database
conn = sqlite3.connect('nba_stats.db')
cur = conn.cursor()

# Create a table to store the team statistics
cur.execute('''CREATE TABLE IF NOT EXISTS team_stats (
    team_id INTEGER,
    year INTEGER,
    three_point_attempts INTEGER,
    three_point_made INTEGER,
    three_point_percentage REAL,
    po_wins INTEGER,
    wins INTEGER,
    losses INTEGER
)''')

# Commit the changes and close the connection
conn.commit()
conn.close()
