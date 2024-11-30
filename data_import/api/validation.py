from typing import Dict, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ValidationError(Exception):
    field: str
    message: str

def validate_player_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and normalize player data"""
    required_fields = ['id', 'fullName', 'position']
    for field in required_fields:
        if field not in data:
            raise ValidationError(field, f'Missing required field: {field}')
    
    # Normalize and validate position
    valid_positions = ['QB', 'RB', 'WR', 'TE', 'K', 'DEF']
    position = data.get('position', '').upper()
    if position not in valid_positions:
        raise ValidationError('position', f'Invalid position: {position}')
    
    return {
        'id': data['id'],
        'name': data['fullName'],
        'position': position,
        'team_id': data.get('teamId'),
        'jersey_number': data.get('jerseyNumber'),
        'status': data.get('status', 'ACTIVE'),
        'height': data.get('height'),
        'weight': data.get('weight'),
        'age': data.get('age'),
        'experience': data.get('experience'),
        'last_updated': datetime.now().isoformat()
    }

def validate_team_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and normalize team data"""
    required_fields = ['id', 'name', 'abbreviation']
    for field in required_fields:
        if field not in data:
            raise ValidationError(field, f'Missing required field: {field}')
    
    return {
        'id': data['id'],
        'name': data['name'],
        'abbreviation': data['abbreviation'],
        'conference': data.get('conference'),
        'division': data.get('division'),
        'venue': data.get('venue', {}).get('name'),
        'head_coach': data.get('headCoach', {}).get('name'),
        'win_loss_record': {
            'wins': data.get('record', {}).get('wins', 0),
            'losses': data.get('record', {}).get('losses', 0),
            'ties': data.get('record', {}).get('ties', 0)
        },
        'last_updated': datetime.now().isoformat()
    }