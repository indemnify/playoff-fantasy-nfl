import pandas as pd
from typing import List, Dict, Optional
from datetime import datetime
import logging
from .api import NFLApiClient, ApiConfig, NFLDataCache, ValidationError

class PlayoffRosterGenerator:
    def __init__(self, cache_dir: str = 'cache'):
        # Initialize API client with config
        api_config = ApiConfig(
            base_url='https://site.api.espn.com/apis/site/v2/sports/football/nfl',
            requests_per_minute=60
        )
        self.cache = NFLDataCache(cache_dir)
        self.api_client = NFLApiClient(api_config, self.cache)
        self.valid_positions = ['QB', 'RB', 'WR', 'TE', 'K', 'DEF']
        self._setup_logging()
    
    def _setup_logging(self):
        self.logger = logging.getLogger('PlayoffRosterGenerator')
        handler = logging.FileHandler('roster_generator.log')
        handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    def get_playoff_teams(self) -> List[Dict]:
        """Get current playoff teams"""
        try:
            return self.api_client.get_playoff_teams()
        except Exception as e:
            self.logger.error(f'Error fetching playoff teams: {str(e)}')
            return []
    
    def get_team_roster(self, team_id: str) -> List[Dict]:
        """Get roster for a specific team"""
        try:
            return self.api_client.get_team_roster(team_id)
        except Exception as e:
            self.logger.error(f'Error fetching roster for team {team_id}: {str(e)}')
            return []
    
    def get_player_status(self, player_id: str) -> Dict:
        """Get player status"""
        try:
            return self.api_client.get_player_status(player_id)
        except Exception as e:
            self.logger.error(f'Error fetching status for player {player_id}: {str(e)}')
            return {'active': True, 'injury_status': None}
    
    def generate_playoff_rosters(self) -> pd.DataFrame:
        """Generate complete playoff rosters with status"""
        all_players = []
        playoff_teams = self.get_playoff_teams()
        
        for team in playoff_teams:
            team_id = team['id']
            playoff_status = self.api_client.get_team_playoff_status(team_id)
            roster = self.get_team_roster(team_id)
            
            for player in roster:
                if player['position'] not in self.valid_positions:
                    continue
                
                status = self.get_player_status(player['id'])
                
                player_data = {
                    'player_id': player['id'],
                    'name': player['name'],
                    'position': player['position'],
                    'team_id': team_id,
                    'team_name': team['name'],
                    'team_abbreviation': team['abbreviation'],
                    'playoff_seed': playoff_status.get('seed'),
                    'active': status.get('active', True),
                    'injury_status': status.get('injury_status'),
                    'jersey_number': player.get('jersey_number'),
                    'experience': player.get('experience'),
                    'last_updated': datetime.now().isoformat()
                }
                all_players.append(player_data)
        
        return pd.DataFrame(all_players)
    
    def filter_by_position(self, df: pd.DataFrame, positions: Optional[List[str]] = None) -> pd.DataFrame:
        """Filter players by position"""
        if positions is None:
            positions = self.valid_positions
        return df[df['position'].isin(positions)]
    
    def export_to_csv(self, df: pd.DataFrame, filename: str) -> None:
        """Export DataFrame to CSV"""
        df.to_csv(filename, index=False)
        self.logger.info(f'Data exported to {filename}')
    
    def run_full_update(self, output_file: str = 'playoff_rosters.csv') -> None:
        """Run complete update process"""
        try:
            # Generate rosters
            self.logger.info('Starting roster generation process')
            rosters_df = self.generate_playoff_rosters()
            
            # Filter by position
            rosters_df = self.filter_by_position(rosters_df)
            
            # Sort by position and team
            rosters_df = rosters_df.sort_values(['position', 'team_abbreviation', 'name'])
            
            # Export to CSV
            self.export_to_csv(rosters_df, output_file)
            self.logger.info('Roster generation completed successfully')
            
        except Exception as e:
            self.logger.error(f'Error in roster generation process: {str(e)}')
            raise

def main():
    generator = PlayoffRosterGenerator()
    generator.run_full_update()

if __name__ == '__main__':
    main()