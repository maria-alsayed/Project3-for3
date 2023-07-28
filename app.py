from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)

# Function to fetch team statistics from the database
def fetch_team_stats():
    conn = sqlite3.connect('nba_stats.db')
    cur = conn.cursor()

    teams_data = []
    for team_id in [1610612759, 1610612752, 1610612744, 1610612737, 1610612738, 1610612747, 1610612739]:
        cur.execute('''SELECT year, three_point_attempts, three_point_made, three_point_percentage, po_wins, wins, losses
            FROM team_stats WHERE team_id=? ORDER BY year''', (team_id,))
        team_data = cur.fetchall()
        teams_data.append({
            'team_id': team_id,
            'team_data': team_data
        })

    conn.close()
    return teams_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def get_data():
    teams_data = fetch_team_stats()
    return jsonify(teams_data)

if __name__ == '__main__':
    app.run(debug=True)
