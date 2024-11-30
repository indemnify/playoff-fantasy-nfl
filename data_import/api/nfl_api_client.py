import requests
import time
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging
from dataclasses import dataclass
from .validation import validate_player_data, validate_team_data
from .cache import NFLDataCache
from .rate_limiter import RateLimiter

@dataclass
class ApiConfig:
    base_url: str
    api_key: Optional[str] = None
    requests_per_minute: int = 60
    timeout: int = 10

class NFLApiClient:
    def __init__(self, config: ApiConfig, cache: NFLDataCache):
        self.config = config
        self.cache = cache
        self.rate_limiter = RateLimiter(config.requests_per_minute)
        self._setup_logging()
    
    def _setup_logging(self):
        self.logger = logging.getLogger('NFLApiClient')
        handler = logging.FileHandler('nfl_api.log')
        handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Make API request with rate limiting and error handling"""
        self.rate_limiter.wait()
        url = f"{self.config.base_url}/{endpoint}"
        headers = {}
        if self.config.api_key:
            headers['Authorization'] = f'Bearer {self.config.api_key}'
        
        try:
            response = requests.get(
                url,
                params=params,
                headers=headers,
                timeout=self.config.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"API request failed: {str(e)}")
            raise
    
    def get_playoff_teams(self) -> List[Dict]:
        """Get current playoff teams with validation"""
        cache_key = 'playoff_teams'
        cached_data = self.cache.get(cache_key)
        if cached_data:
            return cached_data
        
        data = self._make_request('teams', {'filter': 'playoff'})
        teams = [validate_team_data(team) for team in data.get('teams', [])]
        self.cache.set(cache_key, teams)
        return teams
    
    def get_team_roster(self, team_id: str) -> List[Dict]:
        """Get team roster with player validation"""
        cache_key = f'roster_{team_id}'
        cached_data = self.cache.get(cache_key)
        if cached_data:
            return cached_data
        
        data = self._make_request(f'teams/{team_id}/roster')
        players = [validate_player_data(player) for player in data.get('players', [])]
        self.cache.set(cache_key, players)
        return players
    
    def get_player_status(self, player_id: str) -> Dict:
        """Get player active/inactive status"""
        cache_key = f'status_{player_id}'
        cached_data = self.cache.get(cache_key)
        if cached_data:
            return cached_data
        
        data = self._make_request(f'players/{player_id}/status')
        status = {
            'active': data.get('active', True),
            'injury_status': data.get('injury', {}).get('status'),
            'last_update': datetime.now().isoformat()
        }
        self.cache.set(cache_key, status)
        return status
    
    def get_team_playoff_status(self, team_id: str) -> Dict:
        """Get team playoff status and seeding"""
        cache_key = f'playoff_status_{team_id}'
        cached_data = self.cache.get(cache_key)
        if cached_data:
            return cached_data
        
        data = self._make_request(f'teams/{team_id}/playoff-status')
        status = {
            'clinched': data.get('clinched', False),
            'seed': data.get('seed'),
            'division_rank': data.get('divisionRank'),
            'conference_rank': data.get('conferenceRank'),
            'last_update': datetime.now().isoformat()
        }
        self.cache.set(cache_key, status)
        return status