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

 # >>> FUNCTIONS BELOW ARE TESTING PARSER.PY AFTER THE GAME CLASS METHODS [is_valid , __str__ , __eq__] (DAY 4) <<<

"""test_game_creation OK

test_game_validation OK

test_game_str OK

test_game_equality

test_parser_returns_game_objects"""

def test_game_creation():
    """Tests that all Game objects are made into the class Game"""
    game_obj = Game()
    game_obj_full = Game("2007.08.08" , "The Date" , "Canada" , "1" , "Garry Kasparov" , "Hans Niemann" , "1-0")

    assert bool(isinstance(game_obj, Game) and isinstance(game_obj_full, Game))

def test_game_validation():
    """Tests that games can be validated properly (real games v.s insufficient info)"""

    game_obj = Game()
    game_obj_full = Game("2007.08.08", "The Date", "Canada", "1", "Garry Kasparov", "Hans Niemann", "1-0")

    assert game_obj.is_valid() == False
    assert game_obj_full.is_valid() == True

def test_game_str():
    """Tests that the properly formatted game string is returned"""

    #Note of proper format: f"{white} vs {black} | {date} | {result}"
    game_obj = Game()
    game_obj_incomplete = Game("????.??.??" , "*" , "C*" , "*" , "*" , "*" , "?")
    game_obj_full = Game("2007.08.08", "The Date", "Canada", "1", "Garry Kasparov", "Hans Niemann", "1-0")

    assert game_obj.__str__() == "Unknown vs Unknown | ????-??-?? | Unknown"
    assert game_obj_incomplete.__str__() == "Unknown vs Unknown | ????-??-?? | Unknown"
    assert game_obj_full.__str__() == "Garry Kasparov vs Hans Niemann | 2007.08.08 | 1-0"

def test_game_equality():
    """Tests 2 games can be equal"""

    game_obj = Game()
    game_obj_full_1 = Game("2007.08.08", "The Date", "Canada", "1", "Garry Kasparov", "Hans Niemann", "1-0")
    game_obj_full_2 = Game("2007.08.08", "The Date", "Canada", "1", "Garry Kasparov", "Hans Niemann", "1-0")

    assert game_obj_full_1.__eq__(game_obj_full_2) == True
    assert game_obj_full_1.__eq__(game_obj) == False


