# NFL Playoff Fantasy Football Manager

A web application for managing NFL playoff fantasy football rosters. This application allows users to create and manage fantasy football rosters specifically for the NFL playoffs, with unique rules and constraints.

## Features

- Create fantasy football rosters for NFL playoffs
- Validate roster selections based on specific rules:
  - Each roster must include: QB, RB1, RB2, WR1, WR2, WR3, TE, SUPERFLEX, FLEX, Kicker, and Defense
  - Players can only be selected from teams in the playoffs
  - No duplicate team selections allowed (one player per NFL team)
  - Position-specific validation (SUPERFLEX can be QB/RB/WR/TE, FLEX can be RB/WR/TE)
- View existing rosters
- Web interface for roster management
- Data persistence using JSON files

## Project Structure

- `app.py`: Flask web application with routes and API endpoints
- `roster_manager.py`: Core logic for roster management and validation
- `data_import/`: Directory containing data import utilities
- `templates/`: HTML templates for the web interface
- `data/`: Directory for storing roster and player data
- `tests/`: Test suite for the application
- `requirements.txt`: Python dependencies
- `config.yml`: Configuration settings

## Setup

1. Clone the repository:
```bash
git clone https://github.com/indemnify/playoff-fantasy-nfl.git
cd playoff-fantasy-nfl
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Access the application at `http://localhost:5000`

## Usage

1. Navigate to the home page
2. Click "Create Roster" to start a new roster
3. Select players for each position, following the roster rules:
   - One player per NFL playoff team
   - Position-specific requirements
   - Valid position combinations for FLEX and SUPERFLEX spots
4. Submit your roster
5. View your roster using the provided roster ID

## Testing

Run tests using:
```bash
pip install -r requirements-test.txt
python -m pytest tests/
```

## Data Structure

- Players are stored in `data/players.json`
- Rosters are stored in `data/rosters/` as individual JSON files
- Each roster maintains player information, user ID, and creation timestamp

## Technical Details

- Built with Python and Flask
- Uses dataclasses for type safety
- JSON-based data storage
- Modular design with separate roster management and validation logic
- Web interface with dynamic updates
- Comprehensive validation rules for roster creation

## Future Enhancements

- User authentication and authorization
- Scoring system implementation
- League management features
- Real-time stats integration
- Database integration for improved data management
- API documentation