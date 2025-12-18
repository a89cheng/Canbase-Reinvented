**Game Class Stored Information**
- 
- Player names, rating, _federation_ (not included yet!)
- Game result, _moves_ (not included yet!), _ECO_(not included yet!) /opening code
- Tournament "Event" name, location, date, rounds

**Tables in the Database**
- 
1. Player:
   - Columns: id, name, rating, federation
2. Tournament 
   - Columns: id, name, location, start_date, rounds
3. Game 
   - Columns: id, white_player_id, black_player_id, tournament_id, moves, result, date, eco
4. Optional: Opening (likely not to be implemented)
   - Columns: eco, name
- Currently missing: Eco, white and black player IDs (can be CFC or FIDE IDs) 

**Data Types**
- Player.id → integer (primary key)
- Player.name → text
- Player.rating → integer (optional)
- Tournament.start_date → date
- Game.moves → text
- Game.result → char(3)
- Game.eco → char(3)

**Required / Necessary Fields**
-
- Player name = required
  - Player rating, Player IDs will be searched for using the player name
  - Or should it be the opposite way around... search for player with ID...
- Game result = required
  - Part of the PGN... is one of the required fields
- Tournament location = optional

**To be included**
- moves → full PGN moves
- eco → opening code from PGN
- white_player_id / black_player_id → mapped from Player table IDs

**Table Relationships**
-
- Game.white_player_id → Player.id
- Game.black_player_id → Player.id
- Game.tournament_id → Tournament.id
- Optional: Game.eco → Opening.eco

**Game Insertion Logic**
-
1. Check if Player exists by name; if not, insert and get ID
2. Check if Tournament exists by name/date; if not, insert and get ID
3. Insert Game with available IDs and known fields
4. Leave moves, eco, or other missing fields as NULL until Game class is updated