#Test using: pytest tests/test_insert.py

import pytest
from src.db.insert.insert_game import insert_game
from src.db.insert.insert_player import insert_players
from src.db.insert.insert_tournament import insert_tournament
from src.pgn.parser import *
from src.db.connection import create_db_connection
import io , textwrap

def test_insert_players_returns_ids():
    """Tests if insert_players function returns 2 separate ids"""

    sample_pgn = textwrap.dedent("""
            [Event "Sample Event"]
            [Site "Nowhere"]
            [Date "2025.12.13"]
            [Round "1"]
            [White "Alice"]
            [Black "Bob"]
            [Result "1-0"]

            1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 1-0
            """).encode()

    pgn_file = io.BytesIO(sample_pgn)
    string_obj = convert_pgn_file(pgn_file)
    game_list = parse_pgn_file(string_obj)
    game_obj = parse_game(game_list[0])

    # Add a headers dictionary so the insert functions work
    game_obj.headers = {
        "White": game_obj.white,
        "Black": game_obj.black,
        "Event": game_obj.event,
        "Date": game_obj.date,
        "Result": game_obj.result,
        "Round": game_obj.round,
        "Site": game_obj.site,
        "ECO": getattr(game_obj, "eco", None)  # if your game object has ECO
    }

    a,b = insert_players(game_obj)
    assert type(a) == int and type(b) == int
    assert not(a == b)

def test_insert_tournament_returns_ids():
    """Tests if insert_tournament function returns a valid id"""

    sample_pgn = textwrap.dedent("""
            [Event "Sample Event"]
            [Site "Nowhere"]
            [Date "2025.12.13"]
            [Round "1"]
            [White "Alice"]
            [Black "Bob"]
            [Result "1-0"]

            1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 1-0
            """).encode()

    pgn_file = io.BytesIO(sample_pgn)
    string_obj = convert_pgn_file(pgn_file)
    game_list = parse_pgn_file(string_obj)
    game_obj = parse_game(game_list[0])

    # Add a headers dictionary so the insert functions work
    game_obj.headers = {
        "White": game_obj.white,
        "Black": game_obj.black,
        "Event": game_obj.event,
        "Date": game_obj.date,
        "Result": game_obj.result,
        "Round": game_obj.round,
        "Site": game_obj.site,
        "ECO": getattr(game_obj, "eco", None)  # if your game object has ECO
    }

    a = insert_tournament(game_obj)
    assert type(a) == int

def test_insert_game_insertion():
    """Tests the function insert_game actually inserts a game into its corresponding table"""
    sample_pgn = textwrap.dedent("""
                [Event "Sample Event"]
                [Site "Nowhere"]
                [Date "2025.12.13"]
                [Round "1"]
                [White "Alice"]
                [Black "Bob"]
                [Result "1-0"]

                1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 1-0
                """).encode()

    pgn_file = io.BytesIO(sample_pgn)
    string_obj = convert_pgn_file(pgn_file)
    game_list = parse_pgn_file(string_obj)
    game_obj = parse_game(game_list[0])

    # Add a headers dictionary so the insert functions work
    game_obj.headers = {
        "White": game_obj.white,
        "Black": game_obj.black,
        "Event": game_obj.event,
        "Date": game_obj.date,
        "Result": game_obj.result,
        "Round": game_obj.round,
        "Site": game_obj.site,
        "ECO": getattr(game_obj, "eco", None)  # if your game object has ECO
    }

    #Insert the players... or make sure they already are
    white_id , black_id =  insert_players(game_obj)
    tourney_id = insert_tournament(game_obj)

    #Need to check the amount of rows before
    connection = create_db_connection("localhost", "root", "password", "Canbase_Reinvented")
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM Game;")
    count = cursor.fetchone()[0]

    result = insert_game(game_obj, white_id, black_id, tourney_id)

    cursor.execute("SELECT COUNT(*) FROM Game;")
    new_count = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    assert result == None
    assert new_count == count + 1