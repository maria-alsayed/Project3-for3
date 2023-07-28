from flask import Flask, jsonify, render_template
import pandas as pd
from nba_api.stats.endpoints import teamyearbyyearstats

app = Flask(__name__)

# Define a dictionary to store team IDs and their corresponding names
team_names = {
    1610612739: 'Cleveland Cavaliers',
    1610612738: 'Boston Celtics',
    1610612759: 'Spurs',
    1610612747: 'LA Lakers',
    1610612741: 'Bulls',
    1610612752: 'Knicks',
    1610612744: 'Warriors',

    # Add more teams here if needed
}

def get_team_data(team_id):
    try:
        # Retrieve team year-by-year statistics
        team_stats = teamyearbyyearstats.TeamYearByYearStats(team_id=team_id)
        team_stats_df = team_stats.get_data_frames()[0]

        # Filter the relevant columns for three-point attempts made (FG3A), made (FG3M), and percentage (FG3_PCT)
        team_three_point_stats_df = pd.DataFrame({
            'Year': team_stats_df['YEAR'],
            'Three-Point Attempts': team_stats_df['FG3A'],
            'Three-Point Made': team_stats_df['FG3M'],
            'Three-Point Percentage': team_stats_df['FG3_PCT'],
            'Playoff Wins': team_stats_df['PO_WINS']
        })

        # Convert the 'Year' column to integers representing the starting year of the season
        team_three_point_stats_df['Year'] = team_three_point_stats_df['Year'].str[:4].astype(int)

        return team_three_point_stats_df.to_dict(orient='records')
    except:
        return []

# @app.route('/team/<int:team_id>', methods=['GET'])
@app.route('/team/<team_id>', methods=['GET'])
def get_team_stats(team_id):
    team_data = get_team_data(team_id)
    if not team_data:
        return f"Team data for team ID {team_id} not found.", 404
    return jsonify({
        'Team Name': team_names.get(team_id, 'Unknown'),
        'Team Data': team_data
    })

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
