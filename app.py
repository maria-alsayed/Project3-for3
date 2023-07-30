from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)

# Function to fetch team statistics from the database
def fetch_team_stats():
    conn = sqlite3.connect('nba_stats.db')
    cur = conn.cursor()

    teams_data = []
    team_names = {
        1610612739: 'Cleveland Cavaliers',
        1610612738: 'Boston Celtics',
        1610612759: 'San Antonio Spurs',
        1610612747: 'Los Angeles Lakers',
        1610612741: 'Chicago Bulls',
        1610612752: 'New York Knicks',
        1610612744: 'Golden State Warriors'
    }

    for team_id in team_names.keys():
        cur.execute('''SELECT year, three_point_attempts, three_point_made, three_point_percentage, po_wins, wins, losses
            FROM team_stats WHERE team_id=? ORDER BY year''', (team_id,))
        team_data = cur.fetchall()
        teams_data.append({
            'team_id': team_id,
            'team_name': team_names[team_id],
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
