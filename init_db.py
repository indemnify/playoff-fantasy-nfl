import json
from pathlib import Path
from roster_manager import RosterManager

def init_data():
    data_dir = Path('data')
    data_dir.mkdir(exist_ok=True)
    (data_dir / 'rosters').mkdir(exist_ok=True)
    
    # 2024 NFL Playoff Teams and Players
    players = {
        # Ravens
        "BAL_QB1": {
            "id": "BAL_QB1",
            "name": "Lamar Jackson",
            "position": "QB",
            "team": "BAL",
            "projected_points": 25.8
        },
        "BAL_RB1": {
            "id": "BAL_RB1",
            "name": "Keaton Mitchell",
            "position": "RB",
            "team": "BAL",
            "projected_points": 12.4
        },
        "BAL_WR1": {
            "id": "BAL_WR1",
            "name": "Zay Flowers",
            "position": "WR",
            "team": "BAL",
            "projected_points": 14.2
        },
        
        # Bills
        "BUF_QB1": {
            "id": "BUF_QB1",
            "name": "Josh Allen",
            "position": "QB",
            "team": "BUF",
            "projected_points": 26.1
        },
        "BUF_RB1": {
            "id": "BUF_RB1",
            "name": "James Cook",
            "position": "RB",
            "team": "BUF",
            "projected_points": 15.3
        },
        "BUF_WR1": {
            "id": "BUF_WR1",
            "name": "Stefon Diggs",
            "position": "WR",
            "team": "BUF",
            "projected_points": 18.7
        },
        
        # Chiefs
        "KC_QB1": {
            "id": "KC_QB1",
            "name": "Patrick Mahomes",
            "position": "QB",
            "team": "KC",
            "projected_points": 24.9
        },
        "KC_TE1": {
            "id": "KC_TE1",
            "name": "Travis Kelce",
            "position": "TE",
            "team": "KC",
            "projected_points": 16.8
        },
        
        # 49ers
        "SF_QB1": {
            "id": "SF_QB1",
            "name": "Brock Purdy",
            "position": "QB",
            "team": "SF",
            "projected_points": 22.3
        },
        "SF_RB1": {
            "id": "SF_RB1",
            "name": "Christian McCaffrey",
            "position": "RB",
            "team": "SF",
            "projected_points": 23.5
        },
        "SF_WR1": {
            "id": "SF_WR1",
            "name": "Deebo Samuel",
            "position": "WR",
            "team": "SF",
            "projected_points": 17.4
        },
        
        # Cowboys
        "DAL_QB1": {
            "id": "DAL_QB1",
            "name": "Dak Prescott",
            "position": "QB",
            "team": "DAL",
            "projected_points": 23.8
        },
        "DAL_WR1": {
            "id": "DAL_WR1",
            "name": "CeeDee Lamb",
            "position": "WR",
            "team": "DAL",
            "projected_points": 21.2
        },
        
        # Lions
        "DET_QB1": {
            "id": "DET_QB1",
            "name": "Jared Goff",
            "position": "QB",
            "team": "DET",
            "projected_points": 20.5
        },
        "DET_RB1": {
            "id": "DET_RB1",
            "name": "Jahmyr Gibbs",
            "position": "RB",
            "team": "DET",
            "projected_points": 16.8
        },
        "DET_WR1": {
            "id": "DET_WR1",
            "name": "Amon-Ra St. Brown",
            "position": "WR",
            "team": "DET",
            "projected_points": 19.3
        },
        
        # Add team defenses
        "BAL_DEF": {
            "id": "BAL_DEF",
            "name": "Ravens D/ST",
            "position": "DEF",
            "team": "BAL",
            "projected_points": 8.5
        },
        "BUF_DEF": {
            "id": "BUF_DEF",
            "name": "Bills D/ST",
            "position": "DEF",
            "team": "BUF",
            "projected_points": 8.2
        },
        "SF_DEF": {
            "id": "SF_DEF",
            "name": "49ers D/ST",
            "position": "DEF",
            "team": "SF",
            "projected_points": 9.1
        },
        
        # Add kickers
        "BAL_K": {
            "id": "BAL_K",
            "name": "Justin Tucker",
            "position": "K",
            "team": "BAL",
            "projected_points": 9.8
        },
        "SF_K": {
            "id": "SF_K",
            "name": "Jake Moody",
            "position": "K",
            "team": "SF",
            "projected_points": 8.9
        },
        "DAL_K": {
            "id": "DAL_K",
            "name": "Brandon Aubrey",
            "position": "K",
            "team": "DAL",
            "projected_points": 9.2
        }
    }
    
    # Save players data
    with open(data_dir / 'players.json', 'w') as f:
        json.dump(players, f, indent=2)
    
    # Create sample roster
    roster_manager = RosterManager()
    sample_roster = {
        "qb": "BUF_QB1",
        "rb1": "SF_RB1",
        "rb2": "DET_RB1",
        "wr1": "DAL_WR1",
        "wr2": "DET_WR1",
        "wr3": "BUF_WR1",
        "te": "KC_TE1",
        "flex": "BAL_RB1",
        "superflex": "BAL_QB1",
        "kicker": "DAL_K",
        "defense": "SF_DEF"
    }
    
    try:
        roster = roster_manager.create_roster("sample_user", sample_roster)
        print(f"Created sample roster with ID: {roster.id}")
    except Exception as e:
        print(f"Error creating sample roster: {e}")

if __name__ == '__main__':
    print("Initializing database with sample data...")
    init_data()
    print("Done!")
