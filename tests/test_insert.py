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
    game_obj = game_list[0]

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
    game_obj = game_list[0]

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
    game_obj = game_list[0]

    #Insert the players... or make sure they already are
    white_id , black_id =  insert_players(game_obj)
    tourney_id = insert_tournament(game_obj)

    #Need to check the amount of rows before
    connection = create_db_connection("localhost", "root", "password", "Canbase_Reinvented")
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM Game;")
    count = cursor.fetchone()[0]

    game_id = insert_game(game_obj, white_id, black_id, tourney_id)

    # To solve the previous problem, we need to "refresh the connection"
    cursor.close()
    connection.close()
    connection = create_db_connection("localhost", "root", "password", "Canbase_Reinvented")
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM Game;")
    new_count = cursor.fetchone()[0]
    #The problem before was there were 2 different commited versions of the database...

    cursor.close()
    connection.close()

    assert type(game_id) == int
    assert new_count == count + 1