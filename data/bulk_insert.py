#Temporary file | Run with: python -m data.bulk_insert
from src.pgn.parser import *
from src.db.insert.insert_player import insert_players
from src.db.insert.insert_tournament import insert_tournament
from src.db.insert.insert_game import insert_game


def bulk_insert(cursor, pgn_file):
    inserted_count = 0
    skipped_count = 0

    #Allows both an actual file or a file path
    game_pgn = convert_pgn_file(pgn_file)
    games = parse_pgn_file(game_pgn)

    for game in games:
        players = [game.white, game.black]
        if None in players or "?" in players:
            print(f"Skipping game due to missing player: White={game.white}, Black={game.black}")
            continue  # skip this game

        try:
            # ensure both player and tournament are inserted
            white_id, black_id = insert_players(cursor, game)
            tourney_id = insert_tournament(cursor, game)

            # only insert the game if all IDs exist
            if None not in [white_id, black_id, tourney_id]:
                print(f"IDs: white={white_id}, black={black_id}, tourney={tourney_id}")
                insert_game(cursor, game, white_id, black_id, tourney_id)
                inserted_count += 1
            else:
                print(f"Skipping game: missing IDs for {game.white} vs {game.black}")
                skipped_count += 1
        except Exception as e:
            print(f"Unexpected error: {e}")

    print(f"\nSummary: {inserted_count} games inserted, {skipped_count} games skipped")

if __name__ == "__main__":
    pgn_path = "data/2000.pgn"
    bulk_insert(pgn_path)

"""
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS Game;
DROP TABLE IF EXISTS Player;
DROP TABLE IF EXISTS Tournament;
SET FOREIGN_KEY_CHECKS = 1;
"""