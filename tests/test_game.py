#Test using: pytest tests/test_game.py
from src.models.game import Game
import pytest

#Format of the Game Object arguments: (date [], event, site, round_num, white, black, result)

def test_init_valid():
    """Tests all the parameters initialize properly if they're all submitted"""

    game_obj = Game("2007.08.08" , "The Date" , "Canada" , "1" , "Garry Kasparov" , "Hans Niemann" , "1-0")

    assert game_obj.date == "2007.08.08"
    assert game_obj.event == "The Date"
    assert game_obj.site == "Canada"
    assert game_obj.round_num == "1"
    assert game_obj.white == "Garry Kasparov"
    assert game_obj.black == "Hans Niemann"
    assert game_obj.result == "1-0"

def test_init_placeholders():
    """Tests the unknowns are interpreted as None"""

    game_obj = Game("????.??.??", "*", "*", "*", "*", "*", "?")

    assert game_obj.date == None
    assert game_obj.event == None
    assert game_obj.site == None
    assert game_obj.round_num == None
    assert game_obj.white == None
    assert game_obj.black == None
    assert game_obj.result == None

def test_init_defaults():
    """Tests the initialized values are None, if nothing is submitted"""

    game_obj = Game()
    assert game_obj.date == None
    assert game_obj.event == None
    assert game_obj.site == None
    assert game_obj.round_num == None
    assert game_obj.white == None
    assert game_obj.black == None
    assert game_obj.result == None

def test_attributes_exist():
    """Tests the attributes actually exist, even if they are None"""
    game_obj = Game()

    assert hasattr(game_obj, "date")
    assert hasattr(game_obj, "event")
    assert hasattr(game_obj, "site")
    assert hasattr(game_obj, "round_num")
    assert hasattr(game_obj, "white")
    assert hasattr(game_obj, "black")
    assert hasattr(game_obj, "result")