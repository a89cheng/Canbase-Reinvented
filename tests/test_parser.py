"""HOW TO RUN: pytest tests/test_parser.py"""

import pytest
import io
import textwrap
import chess
import chess.pgn
from src.pgn.parser import convert_pgn_file , parse_pgn_file , parse_game

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

def test_dictionary_returned_with_elements():
    """Tests a dictionary is returned, and tests that the headers are all part of the dictionary
    either being in their proper forms, or marked as Unknown"""

    #Textwrap enables the format of the string to be consistent
    sample_pgn_1 = textwrap.dedent("""
    [Event "Sample Event"]
    [Site "Nowhere"]
    [Date "2025.12.13"]
    [Round "1"]
    [White "Alice"]
    [Black "Bob"]
    [Result "1-0"]

    1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 1-0
    """).encode()

    sample_pgn_2 = b"""
    1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 1-0
    """

    # Test first PGN with full headers
    pgn_file = io.BytesIO(sample_pgn_1)
    string_obj = convert_pgn_file(pgn_file)
    game_list = parse_pgn_file(string_obj)
    result = parse_game(game_list[0])

    # Assert type
    assert isinstance(result, dict)

    # Assert mandatory keys exist
    expected_keys = {
        "Date", "Event", "Round",
        "White", "White Elo", "Black", "Black Elo",
        "Result", "Opening"
    }
    assert expected_keys.issubset(result.keys())

    # Assert known header values
    assert result["White"] == "Alice"
    assert result["Black"] == "Bob"
    assert result["Date"] == "2025.12.13"
    assert result["Result"] == "1-0"
    assert result["Round"] == "1"

    # Test second PGN with missing headers
    pgn_file = io.BytesIO(sample_pgn_2)
    string_obj = convert_pgn_file(pgn_file)
    game_list = parse_pgn_file(string_obj)
    result = parse_game(game_list[0])

    # Assert missing headers default to something (Unknown or similar)
    for key in expected_keys:
        assert key in result
        assert result[key] is not None  # allows "Unknown" or any placeholder