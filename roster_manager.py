from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import json
import os
import uuid
from pathlib import Path

@dataclass
class Player:
    id: str
    name: str
    position: str
    team: str
    projected_points: float = 0.0

@dataclass
class Roster:
    id: str
    user_id: str
    team_id: str
    qb: Player
    rb1: Player
    rb2: Player
    wr1: Player
    wr2: Player
    wr3: Player
    te: Player
    superflex: Player
    flex: Player
    kicker: Player
    defense: Player
    created_at: datetime

class RosterValidationError(Exception):
    pass

class RosterValidator:
    VALID_POSITIONS = ['QB', 'RB', 'WR', 'TE', 'K', 'DEF']
    SUPERFLEX_POSITIONS = ['QB', 'RB', 'WR', 'TE']
    FLEX_POSITIONS = ['RB', 'WR', 'TE']

    @staticmethod
    def validate_player_position(player: Player, required_position: str) -> bool:
        """Validate player is eligible for the required position"""
        if required_position == 'SUPERFLEX':
            return player.position in RosterValidator.SUPERFLEX_POSITIONS
        elif required_position == 'FLEX':
            return player.position in RosterValidator.FLEX_POSITIONS
        return player.position == required_position

    @staticmethod
    def validate_unique_teams(roster: Dict[str, Player]) -> bool:
        """Ensure no team is used more than once"""
        teams = set()
        for player in roster.values():
            if player.team in teams:
                return False
            teams.add(player.team)
        return True

class RosterManager:
    def __init__(self, data_dir: str = 'data'):
        self.data_dir = Path(data_dir)
        self.rosters_dir = self.data_dir / 'rosters'
        self.players_file = self.data_dir / 'players.json'
        self._ensure_directories()
        self.validator = RosterValidator()

    def _ensure_directories(self):
        """Create necessary directories if they don't exist"""
        self.data_dir.mkdir(exist_ok=True)
        self.rosters_dir.mkdir(exist_ok=True)

    def _player_to_dict(self, player: Player) -> Dict:
        """Convert Player object to dictionary with enhanced stats"""
        if not player:
            return None
            
        return {
            'id': player.id,
            'name': player.name,
            'position': player.position,
            'team': player.team,
            'projected_points': player.projected_points,
            'stats': {
                'games_played': 17,
                'rushing_yards': 0,
                'rushing_tds': 0,
                'receiving_yards': 0,
                'receiving_tds': 0,
                'passing_yards': 0,
                'passing_tds': 0,
                'interceptions': 0,
                'fumbles': 0,
                'avg_points': player.projected_points,
                'last_5_games': [0, 0, 0, 0, 0]
            }
        }

    def create_roster(self, user_id: str, roster_data: Dict) -> Roster:
        """Create a new roster for a user"""
        try:
            # Convert raw data to Player objects
            players = {}
            for position, player_id in roster_data.items():
                player_info = self._get_player_info(player_id)
                players[position] = Player(
                    id=player_id,
                    name=player_info['name'],
                    position=player_info['position'],
                    team=player_info['team'],
                    projected_points=player_info.get('projected_points', 0.0)
                )

            # Validate positions
            if not self.validator.validate_player_position(players['qb'], 'QB'):
                raise RosterValidationError("Invalid QB selection")
            
            for pos in ['rb1', 'rb2']:
                if not self.validator.validate_player_position(players[pos], 'RB'):
                    raise RosterValidationError(f"Invalid {pos.upper()} selection")
            
            for pos in ['wr1', 'wr2', 'wr3']:
                if not self.validator.validate_player_position(players[pos], 'WR'):
                    raise RosterValidationError(f"Invalid {pos.upper()} selection")
            
            if not self.validator.validate_player_position(players['te'], 'TE'):
                raise RosterValidationError("Invalid TE selection")
            
            if not self.validator.validate_player_position(players['superflex'], 'SUPERFLEX'):
                raise RosterValidationError("Invalid SUPERFLEX selection")
            
            if not self.validator.validate_player_position(players['flex'], 'FLEX'):
                raise RosterValidationError("Invalid FLEX selection")
            
            if not self.validator.validate_player_position(players['kicker'], 'K'):
                raise RosterValidationError("Invalid Kicker selection")
            
            if not self.validator.validate_player_position(players['defense'], 'DEF'):
                raise RosterValidationError("Invalid Defense selection")

            # Validate unique teams
            if not self.validator.validate_unique_teams(players):
                raise RosterValidationError("Cannot select multiple players from the same team")

            # Create roster object
            roster = Roster(
                id=str(uuid.uuid4()),
                user_id=user_id,
                team_id=user_id,  # You might want to make this configurable
                qb=players['qb'],
                rb1=players['rb1'],
                rb2=players['rb2'],
                wr1=players['wr1'],
                wr2=players['wr2'],
                wr3=players['wr3'],
                te=players['te'],
                superflex=players['superflex'],
                flex=players['flex'],
                kicker=players['kicker'],
                defense=players['defense'],
                created_at=datetime.now()
            )

            # Save roster
            self._save_roster(roster)
            return roster

        except (FileNotFoundError, ValueError, KeyError) as e:
            raise RosterValidationError(f"Error creating roster: {str(e)}")

    def _save_roster(self, roster: Roster):
        """Save roster to file"""
        roster_file = self.rosters_dir / f"{roster.id}.json"
        roster_data = {
            'id': roster.id,
            'user_id': roster.user_id,
            'team_id': roster.team_id,
            'created_at': roster.created_at.isoformat(),
            'players': {
                'qb': self._player_to_dict(roster.qb),
                'rb1': self._player_to_dict(roster.rb1),
                'rb2': self._player_to_dict(roster.rb2),
                'wr1': self._player_to_dict(roster.wr1),
                'wr2': self._player_to_dict(roster.wr2),
                'wr3': self._player_to_dict(roster.wr3),
                'te': self._player_to_dict(roster.te),
                'superflex': self._player_to_dict(roster.superflex),
                'flex': self._player_to_dict(roster.flex),
                'kicker': self._player_to_dict(roster.kicker),
                'defense': self._player_to_dict(roster.defense)
            }
        }

        with open(roster_file, 'w') as f:
            json.dump(roster_data, f, indent=2)

    def get_roster(self, roster_id: str) -> Optional[Roster]:
        """Retrieve a roster by ID"""
        roster_file = self.rosters_dir / f"{roster_id}.json"
        if not roster_file.exists():
            return None

        with open(roster_file, 'r') as f:
            data = json.load(f)
            return self._dict_to_roster(data)

    def _dict_to_roster(self, data: Dict) -> Roster:
        """Convert dictionary to Roster object"""
        players = data['players']
        return Roster(
            id=data['id'],
            user_id=data['user_id'],
            team_id=data.get('team_id', data['user_id']),
            created_at=datetime.fromisoformat(data['created_at']),
            qb=self._dict_to_player(players['qb']),
            rb1=self._dict_to_player(players['rb1']),
            rb2=self._dict_to_player(players['rb2']),
            wr1=self._dict_to_player(players['wr1']),
            wr2=self._dict_to_player(players['wr2']),
            wr3=self._dict_to_player(players['wr3']),
            te=self._dict_to_player(players['te']),
            superflex=self._dict_to_player(players['superflex']),
            flex=self._dict_to_player(players['flex']),
            kicker=self._dict_to_player(players['kicker']),
            defense=self._dict_to_player(players['defense'])
        )

    def _dict_to_player(self, data: Dict) -> Player:
        """Convert dictionary to Player object"""
        if not data:
            return None
            
        return Player(
            id=data['id'],
            name=data['name'],
            position=data['position'],
            team=data['team'],
            projected_points=data.get('projected_points', 0.0)
        )

    def get_user_rosters(self, user_id: str) -> List[Roster]:
        """Get all rosters for a user"""
        rosters = []
        for roster_file in self.rosters_dir.glob("*.json"):
            with open(roster_file, 'r') as f:
                data = json.load(f)
                if data['user_id'] == user_id:
                    rosters.append(self._dict_to_roster(data))
        return rosters