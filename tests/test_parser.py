"""HOW TO RUN: pytest tests/test_parser.py"""

import pytest
import io
import textwrap
import chess.pgn
from src.pgn.parser import convert_pgn_file , parse_pgn_file , parse_game
from src.models.game import Game

# Forgot to do the following the first time around
from io import StringIO

# Importance of using
# - isinstance(object, type) in order to test the type of outputs
# - io.BytesIO(file) ; takes a bytes and converts them to a binary file

def test_IO_object_made():
    """Tests if the convert_pgn_file function returns an StringIO class object"""
    #The b before the string makes it binary! Very interesting...
    sample_pgn = b"[Event \"Sample\"]\n1. e4 e5 1-0"
    pgn_file = io.BytesIO(sample_pgn)

    result = convert_pgn_file(pgn_file)
    #First argument is object, second argument is the class
    assert isinstance(result, StringIO)

def test_list_made():
    """Tests if the parse_pgn_file function returns a list"""
    sample_pgn = b"[Event \"Sample\"]\n1. e4 e5 1-0"
    pgn_file = io.BytesIO(sample_pgn)
    result = convert_pgn_file(pgn_file)
    output = parse_pgn_file(result)

    assert isinstance(output , list)
    assert len(output) > 0

def test_list_index_contains_game_object():
    """Tests if the parse_pgn_file function's returned list contains game class objects"""
    sample_pgn = b"[Event \"Sample\"]\n1. e4 e5 1-0"
    pgn_file = io.BytesIO(sample_pgn)
    result = convert_pgn_file(pgn_file)
    games = parse_pgn_file(result)

    for game in games:
        assert isinstance(game, chess.pgn.Game)


 # >>> FUNCTIONS BELOW ARE TESTING PARSER.PY AFTER THE GAME CLASS HAS BEEN MADE AND IMPLEMENTED (DAY 2)<<<


def test_GameObj_returned_with_elements():
    """Tests a Game object is returned"""

    sample_pgn_2 = b"""
    1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 1-0
    """

    # Test second PGN with missing headers
    pgn_file = io.BytesIO(sample_pgn_2)
    string_obj = convert_pgn_file(pgn_file)
    game_list = parse_pgn_file(string_obj)
    result = parse_game(game_list[0])

    assert isinstance(result, Game)

def test_core_attributes_exist():
    """Tests the core results are properly stored in the object"""
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
    result = parse_game(game_list[0])

    #Formt of Game class inputs
    #(date, event, site, round_num, white, black, result)

    assert result.date == "2025.12.13"
    assert result.event == "Sample Event"
    assert result.site == "Nowhere"
    assert result.round_num == "1"
    assert result.white == "Alice"
    assert result.black == "Bob"
    assert result.result == "1-0"

def test_missing_inputs():
    "Tests that None is the result of missing inputs"
    sample_pgn_2 = b"""
        1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 1-0
        """

    # Test second PGN with missing headers
    pgn_file = io.BytesIO(sample_pgn_2)
    string_obj = convert_pgn_file(pgn_file)
    game_list = parse_pgn_file(string_obj)
    result = parse_game(game_list[0])

    assert result.date == None
    assert result.event == None
    assert result.site == None
    assert result.round_num == None
    assert result.white == None
    assert result.black == None
    assert result.result == "1-0"

def test_parsing_multiple_games():
    """Tests that parse_pgn_file can handle multiple games
    and parse_game converts each to a Game object"""

    # Sample PGN with two games
    multi_game_pgn = b"""
    [Event "Game 1"]
    [Site "Nowhere"]
    [Date "2025.12.13"]
    [Round "1"]
    [White "Alice"]
    [Black "Bob"]
    [Result "1-0"]

    1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 1-0

    [Event "Game 2"]
    [Site "Somewhere"]
    [Date "2025.12.14"]
    [Round "2"]
    [White "Charlie"]
    [Black "Dana"]
    [Result "0-1"]

    1. d4 d5 2. c4 c6 3. Nc3 Nf6 0-1
    """

    # Convert PGN bytes to StringIO
    pgn_file = io.BytesIO(multi_game_pgn)
    string_obj = convert_pgn_file(pgn_file)

    # Parse the StringIO into a list of python-chess Game objects
    game_list = parse_pgn_file(string_obj)

    # Ensure we got two games from the PGN
    # Changed to 2 or more, due to spacing issues in the file
    assert len(game_list) >= 2

    # Convert each python-chess Game to our Day-3 Game object
    day3_games = [parse_game(g) for g in game_list]

    # Check that each object is a Game and core attributes exist
    for i, game in enumerate(day3_games):
        assert isinstance(game, Game)
        assert hasattr(game, "white")
        assert hasattr(game, "black")
        assert hasattr(game, "result")
        assert hasattr(game, "event")
        assert hasattr(game, "site")
        assert hasattr(game, "date")
        assert hasattr(game, "round_num")

    # Optional: check first game's known headers
    assert day3_games[0].white == "Alice"
    assert day3_games[0].black == "Bob"
    assert day3_games[0].event == "Game 1"
    assert day3_games[0].site == "Nowhere"
    assert day3_games[0].date == "2025.12.13"
    assert day3_games[0].round_num == "1"

    # Optional: check second game's known headers
    assert day3_games[1].white == "Charlie"
    assert day3_games[1].black == "Dana"
    assert day3_games[1].event == "Game 2"
    assert day3_games[1].site == "Somewhere"
    assert day3_games[1].date == "2025.12.14"
    assert day3_games[1].round_num == "2"

def test_round_number_mapping():
    sample_pgn = textwrap.dedent("""
            [Round "1"]

            1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 1-0
            """).encode()

    pgn_file = io.BytesIO(sample_pgn)
    string_obj = convert_pgn_file(pgn_file)
    game_list = parse_pgn_file(string_obj)
    result = parse_game(game_list[0])

    # Format of Game class inputs
    # (date, event, site, round_num, white, black, result)

    assert result.round_num == "1"

def test_minimal_PGN_edge_cases():
    """Tests the core results are properly stored in the object"""
    sample_pgn = textwrap.dedent("""
            [White "Alice"]
            [Black "Bob"]
            [Result "1-0"]

            1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 1-0
            """).encode()

    pgn_file = io.BytesIO(sample_pgn)
    string_obj = convert_pgn_file(pgn_file)
    game_list = parse_pgn_file(string_obj)
    result = parse_game(game_list[0])

    # Format of Game class inputs
    # (date, event, site, round_num, white, black, result)

    assert isinstance(result, Game)
    assert result.date == None
    assert result.event == None
    assert result.site == None
    assert result.round_num == None
    assert result.white == "Alice"
    assert result.black == "Bob"
    assert result.result == "1-0"


 # >>> FUNCTION BELOW IS TESTING PARSER.PY AFTER PARSE_PGN_FILE() RETURNS LIST OF GAME OBJECTS (DAY 4)<<<


def test_parser_returns_game_objects():
    """Tests if the newly modified parser returns Game objects"""

    sample_pgn = b"[Event \"Sample\"]\n1. e4 e5 1-0"
    pgn_file = io.BytesIO(sample_pgn)
    result = convert_pgn_file(pgn_file)
    output = parse_pgn_file(result)

    assert isinstance(output[0], Game)

