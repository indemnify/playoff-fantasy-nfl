import pandas as pd
import json
from pathlib import Path
from typing import Dict, List

class PlayoffRosterGenerator:
    def __init__(self, data_dir: str = 'data'):
        self.data_dir = Path(data_dir)
        self.players_file = self.data_dir / 'players.json'
        self._ensure_directories()
        
        # 2024 Playoff Teams (you can update this each year)
        self.playoff_teams = {
            'BAL': {'name': 'Baltimore Ravens', 'conference': 'AFC', 'seed': 1},
            'BUF': {'name': 'Buffalo Bills', 'conference': 'AFC', 'seed': 2},
            'KC': {'name': 'Kansas City Chiefs', 'conference': 'AFC', 'seed': 3},
            'HOU': {'name': 'Houston Texans', 'conference': 'AFC', 'seed': 4},
            'CLE': {'name': 'Cleveland Browns', 'conference': 'AFC', 'seed': 5},
            'MIA': {'name': 'Miami Dolphins', 'conference': 'AFC', 'seed': 6},
            'PIT': {'name': 'Pittsburgh Steelers', 'conference': 'AFC', 'seed': 7},
            'SF': {'name': 'San Francisco 49ers', 'conference': 'NFC', 'seed': 1},
            'DAL': {'name': 'Dallas Cowboys', 'conference': 'NFC', 'seed': 2},
            'DET': {'name': 'Detroit Lions', 'conference': 'NFC', 'seed': 3},
            'TB': {'name': 'Tampa Bay Buccaneers', 'conference': 'NFC', 'seed': 4},
            'PHI': {'name': 'Philadelphia Eagles', 'conference': 'NFC', 'seed': 5},
            'LAR': {'name': 'Los Angeles Rams', 'conference': 'NFC', 'seed': 6},
            'GB': {'name': 'Green Bay Packers', 'conference': 'NFC', 'seed': 7}
        }

    def _ensure_directories(self):
        """Create necessary directories if they don't exist"""
        self.data_dir.mkdir(exist_ok=True)

    def generate_playoff_rosters(self) -> pd.DataFrame:
        """Generate and return playoff rosters as a DataFrame"""
        players_data = self._generate_sample_players()
        self._save_players(players_data)
        return pd.DataFrame(players_data.values())

    def _generate_sample_players(self) -> Dict:
        """Generate sample players for each playoff team"""
        players = {}
        player_id = 1

        # Sample players for each team
        for team_code, team_info in self.playoff_teams.items():
            # Add QBs
            players[str(player_id)] = {
                'id': str(player_id),
                'name': f'QB1 {team_code}',
                'position': 'QB',
                'team': team_code,
                'team_name': team_info['name'],
                'projected_points': 20.0
            }
            player_id += 1

            # Add RBs
            for i in range(2):
                players[str(player_id)] = {
                    'id': str(player_id),
                    'name': f'RB{i+1} {team_code}',
                    'position': 'RB',
                    'team': team_code,
                    'team_name': team_info['name'],
                    'projected_points': 15.0
                }
                player_id += 1

            # Add WRs
            for i in range(3):
                players[str(player_id)] = {
                    'id': str(player_id),
                    'name': f'WR{i+1} {team_code}',
                    'position': 'WR',
                    'team': team_code,
                    'team_name': team_info['name'],
                    'projected_points': 12.0
                }
                player_id += 1

            # Add TE
            players[str(player_id)] = {
                'id': str(player_id),
                'name': f'TE1 {team_code}',
                'position': 'TE',
                'team': team_code,
                'team_name': team_info['name'],
                'projected_points': 10.0
            }
            player_id += 1

            # Add K
            players[str(player_id)] = {
                'id': str(player_id),
                'name': f'K1 {team_code}',
                'position': 'K',
                'team': team_code,
                'team_name': team_info['name'],
                'projected_points': 8.0
            }
            player_id += 1

            # Add DEF
            players[str(player_id)] = {
                'id': str(player_id),
                'name': f'{team_code} Defense',
                'position': 'DEF',
                'team': team_code,
                'team_name': team_info['name'],
                'projected_points': 8.0
            }
            player_id += 1

        return players

    def _save_players(self, players: Dict):
        """Save players data to JSON file"""
        with open(self.players_file, 'w') as f:
            json.dump(players, f, indent=2)

    def get_players_by_position(self, position: str) -> List[Dict]:
        """Get all players of a specific position"""
        with open(self.players_file, 'r') as f:
            players = json.load(f)
        return [p for p in players.values() if p['position'] == position]

    def get_all_players(self) -> Dict:
        """Get all players from the JSON file"""
        with open(self.players_file, 'r') as f:
            return json.load(f)
