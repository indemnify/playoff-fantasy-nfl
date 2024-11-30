import pandas as pd
import requests
from datetime import datetime
import os

class NFLStatsImporter:
    def __init__(self):
        self.base_url = 'https://site.api.espn.com/apis/site/v2/sports/football/nfl'
        self.data_dir = 'data'
        self._ensure_data_directory()
    
    def _ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def fetch_team_stats(self):
        """Fetch team statistics from ESPN API"""
        url = f'{self.base_url}/teams'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f'Failed to fetch team stats: {response.status_code}')
    
    def fetch_player_stats(self, team_id):
        """Fetch player statistics for a specific team"""
        url = f'{self.base_url}/teams/{team_id}/roster'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f'Failed to fetch player stats: {response.status_code}')
    
    def process_team_stats(self, raw_data):
        """Process raw team statistics into a pandas DataFrame"""
        teams_data = []
        for team in raw_data['sports'][0]['leagues'][0]['teams']:
            team_info = team['team']
            teams_data.append({
                'team_id': team_info['id'],
                'name': team_info['name'],
                'abbreviation': team_info['abbreviation'],
                'location': team_info['location'],
                'wins': team_info.get('record', {}).get('wins', 0),
                'losses': team_info.get('record', {}).get('losses', 0)
            })
        return pd.DataFrame(teams_data)
    
    def save_data(self, df, filename):
        """Save processed data to CSV"""
        filepath = os.path.join(self.data_dir, filename)
        df.to_csv(filepath, index=False)
        print(f'Data saved to {filepath}')

    def run_import(self):
        """Run the full import process"""
        try:
            # Fetch and save team stats
            print('Fetching team stats...')
            team_data = self.fetch_team_stats()
            teams_df = self.process_team_stats(team_data)
            self.save_data(teams_df, f'team_stats_{datetime.now().strftime("%Y%m%d")}.csv')
            
            # Fetch player stats for each team
            print('Fetching player stats...')
            all_players = []
            for team_id in teams_df['team_id']:
                try:
                    player_data = self.fetch_player_stats(team_id)
                    # Process player data here
                    # Add to all_players list
                except Exception as e:
                    print(f'Error fetching players for team {team_id}: {e}')
            
            if all_players:
                players_df = pd.DataFrame(all_players)
                self.save_data(players_df, f'player_stats_{datetime.now().strftime("%Y%m%d")}.csv')
            
            print('Import completed successfully')
            return True
        
        except Exception as e:
            print(f'Error during import: {e}')
            return False

if __name__ == '__main__':
    importer = NFLStatsImporter()
    importer.run_import()