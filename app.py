from flask import Flask, render_template, request, jsonify, session
from roster_manager import RosterManager, RosterValidationError
from data_import.playoff_roster_generator import PlayoffRosterGenerator
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev')

roster_manager = RosterManager()
playoff_generator = PlayoffRosterGenerator()

@app.route('/')
def home():
    return render_template('base.html', last_updated=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

@app.route('/create-roster')
def create_roster():
    # Get available players from the playoff generator
    players_df = playoff_generator.generate_playoff_rosters()
    
    # Convert DataFrame to list of dictionaries
    players = players_df.to_dict('records')
    
    return render_template(
        'create_roster.html',
        players=players,
        last_updated=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )

@app.route('/api/submit-roster', methods=['POST'])
def submit_roster():
    try:
        # Get user ID from session (in production, this would come from authentication)
        user_id = session.get('user_id', 'test_user')
        
        # Create roster
        roster = roster_manager.create_roster(user_id, request.json)
        
        return jsonify({
            'success': True,
            'roster_id': roster.id
        })
        
    except RosterValidationError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'An unexpected error occurred'
        }), 500

@app.route('/roster/<roster_id>')
def view_roster(roster_id):
    roster = roster_manager.get_roster(roster_id)
    if not roster:
        return 'Roster not found', 404
    
    return render_template(
        'view_roster.html',
        roster=roster,
        last_updated=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )

if __name__ == '__main__':
    app.run(debug=True)