import pandas as pd
from nfl_stats_import import NFLStatsImporter
from typing import List, Dict
import os

class PlayoffRosterGenerator:
    def __init__(self):
        self.importer = NFLStatsImporter()
        self.valid_positions = ['QB', 'RB', 'WR', 'TE', 'K', 'DEF']
        self._ensure_data_directory()
    
    def _ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        if not os.path.exists('data'):
            os.makedirs('data')
    
    def get_playoff_teams(self, year: int) -> List[Dict]:
        """Get list of playoff teams for a specific year"""
        # This would normally come from an API, but for 2023 we'll hardcode
        if year == 2023:
            return [
                {'team_id': 'BAL', 'name': 'Baltimore Ravens', 'conference': 'AFC', 'seed': 1},
                {'team_id': 'BUF', 'name': 'Buffalo Bills', 'conference': 'AFC', 'seed': 2},
                {'team_id': 'KC', 'name': 'Kansas City Chiefs', 'conference': 'AFC', 'seed': 3},
                {'team_id': 'HOU', 'name': 'Houston Texans', 'conference': 'AFC', 'seed': 4},
                {'team_id': 'CLE', 'name': 'Cleveland Browns', 'conference': 'AFC', 'seed': 5},
                {'team_id': 'MIA', 'name': 'Miami Dolphins', 'conference': 'AFC', 'seed': 6},
                {'team_id': 'PIT', 'name': 'Pittsburgh Steelers', 'conference': 'AFC', 'seed': 7},
                {'team_id': 'SF', 'name': 'San Francisco 49ers', 'conference': 'NFC', 'seed': 1},
                {'team_id': 'DAL', 'name': 'Dallas Cowboys', 'conference': 'NFC', 'seed': 2},
                {'team_id': 'DET', 'name': 'Detroit Lions', 'conference': 'NFC', 'seed': 3},
                {'team_id': 'TB', 'name': 'Tampa Bay Buccaneers', 'conference': 'NFC', 'seed': 4},
                {'team_id': 'PHI', 'name': 'Philadelphia Eagles', 'conference': 'NFC', 'seed': 5},
                {'team_id': 'LAR', 'name': 'Los Angeles Rams', 'conference': 'NFC', 'seed': 6},
                {'team_id': 'GB', 'name': 'Green Bay Packers', 'conference': 'NFC', 'seed': 7}
            ]
        else:
            raise ValueError(f'Playoff team data not available for year {year}')
    
    def generate_playoff_players_2023(self) -> pd.DataFrame:
        """Generate sample playoff players list for 2023"""
        players_data = [
            # Ravens
            {'name': 'Lamar Jackson', 'position': 'QB', 'team': 'BAL'},
            {'name': 'Justin Tucker', 'position': 'K', 'team': 'BAL'},
            {'name': 'Zay Flowers', 'position': 'WR', 'team': 'BAL'},
            {'name': 'Odell Beckham Jr.', 'position': 'WR', 'team': 'BAL'},
            {'name': 'Justice Hill', 'position': 'RB', 'team': 'BAL'},
            {'name': 'Mark Andrews', 'position': 'TE', 'team': 'BAL'},
            {'name': 'Baltimore Ravens', 'position': 'DEF', 'team': 'BAL'},
            
            # Bills
            {'name': 'Josh Allen', 'position': 'QB', 'team': 'BUF'},
            {'name': 'Tyler Bass', 'position': 'K', 'team': 'BUF'},
            {'name': 'Stefon Diggs', 'position': 'WR', 'team': 'BUF'},
            {'name': 'Gabe Davis', 'position': 'WR', 'team': 'BUF'},
            {'name': 'James Cook', 'position': 'RB', 'team': 'BUF'},
            {'name': 'Dalton Kincaid', 'position': 'TE', 'team': 'BUF'},
            {'name': 'Buffalo Bills', 'position': 'DEF', 'team': 'BUF'},
            
            # Chiefs
            {'name': 'Patrick Mahomes', 'position': 'QB', 'team': 'KC'},
            {'name': 'Harrison Butker', 'position': 'K', 'team': 'KC'},
            {'name': 'Rashee Rice', 'position': 'WR', 'team': 'KC'},
            {'name': 'Isiah Pacheco', 'position': 'RB', 'team': 'KC'},
            {'name': 'Travis Kelce', 'position': 'TE', 'team': 'KC'},
            {'name': 'Kansas City Chiefs', 'position': 'DEF', 'team': 'KC'},
            
            # 49ers
            {'name': 'Brock Purdy', 'position': 'QB', 'team': 'SF'},
            {'name': 'Jake Moody', 'position': 'K', 'team': 'SF'},
            {'name': 'Deebo Samuel', 'position': 'WR', 'team': 'SF'},
            {'name': 'Brandon Aiyuk', 'position': 'WR', 'team': 'SF'},
            {'name': 'Christian McCaffrey', 'position': 'RB', 'team': 'SF'},
            {'name': 'George Kittle', 'position': 'TE', 'team': 'SF'},
            {'name': 'San Francisco 49ers', 'position': 'DEF', 'team': 'SF'},
            
            # Cowboys
            {'name': 'Dak Prescott', 'position': 'QB', 'team': 'DAL'},
            {'name': 'Brandon Aubrey', 'position': 'K', 'team': 'DAL'},
            {'name': 'CeeDee Lamb', 'position': 'WR', 'team': 'DAL'},
            {'name': 'Tony Pollard', 'position': 'RB', 'team': 'DAL'},
            {'name': 'Jake Ferguson', 'position': 'TE', 'team': 'DAL'},
            {'name': 'Dallas Cowboys', 'position': 'DEF', 'team': 'DAL'},
            
            # Lions
            {'name': 'Jared Goff', 'position': 'QB', 'team': 'DET'},
            {'name': 'Riley Patterson', 'position': 'K', 'team': 'DET'},
            {'name': 'Amon-Ra St. Brown', 'position': 'WR', 'team': 'DET'},
            {'name': 'Jameson Williams', 'position': 'WR', 'team': 'DET'},
            {'name': 'David Montgomery', 'position': 'RB', 'team': 'DET'},
            {'name': 'Jahmyr Gibbs', 'position': 'RB', 'team': 'DET'},
            {'name': 'Sam LaPorta', 'position': 'TE', 'team': 'DET'},
            {'name': 'Detroit Lions', 'position': 'DEF', 'team': 'DET'},
            
            # Eagles
            {'name': 'Jalen Hurts', 'position': 'QB', 'team': 'PHI'},
            {'name': 'Jake Elliott', 'position': 'K', 'team': 'PHI'},
            {'name': 'AJ Brown', 'position': 'WR', 'team': 'PHI'},
            {'name': 'DeVonta Smith', 'position': 'WR', 'team': 'PHI'},
            {'name': 'D\'Andre Swift', 'position': 'RB', 'team': 'PHI'},
            {'name': 'Dallas Goedert', 'position': 'TE', 'team': 'PHI'},
            {'name': 'Philadelphia Eagles', 'position': 'DEF', 'team': 'PHI'}
        ]
        
        return pd.DataFrame(players_data)
    
    def filter_by_position(self, df: pd.DataFrame, positions: List[str] = None) -> pd.DataFrame:
        """Filter players by position"""
        if positions is None:
            positions = self.valid_positions
        return df[df['position'].isin(positions)]
    
    def export_to_csv(self, df: pd.DataFrame, filename: str) -> None:
        """Export DataFrame to CSV"""
        df.to_csv(filename, index=False)
        print(f'Data exported to {filename}')

def main():
    generator = PlayoffRosterGenerator()
    
    # Get 2023 playoff teams
    playoff_teams = generator.get_playoff_teams(2023)
    print(f'Found {len(playoff_teams)} playoff teams')
    
    # Generate player list
    players_df = generator.generate_playoff_players_2023()
    
    # Filter by position if needed
    players_df = generator.filter_by_position(players_df)
    
    # Sort by position and team
    players_df = players_df.sort_values(['position', 'team', 'name'])
    
    # Export to CSV
    generator.export_to_csv(players_df, 'data/2023_playoff_players.csv')

if __name__ == '__main__':
    main()