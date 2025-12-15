import io
import chess
import chess.pgn
from src.models.game import Game

def convert_pgn_file(pgn_file):
    """
    Convert a binary PGN file into a file-like text object suitable for parsing.
    Input: pgn_file: a binary file object containing PGN data.
    Output: A StringIO object containing the decoded text from the PGN file,
            which can be read sequentially by the parser.
    """

    text = pgn_file.read().decode("utf-8")
    pgn_text = io.StringIO(text)

    return pgn_text

def parse_pgn_file(pgn_text):
    """
    Split a file-like text object containing PGN data into individual Game objects.
    Input: pgn_text; a file-like text object (StringIO) containing one or more PGN games.
    Output: A list of python-chess Game objects, one per game in the PGN.
    """

    # Resets the file pointer
    pgn_text.seek(0)

    games = []

    while True:
        #Only 1 game is being read at a time
        game = chess.pgn.read_game(pgn_text)
        #If there are no more games left... allowed by python chess
        if game is None:
            break

        # Games are added to the game list, no headers are stored yet
        games.append(game)

    return games

def parse_game(game_string):
    """
    Extract relevant information from a python-chess Game object into a structured dictionary.
    Input: game_object: a single python-chess Game object.
    Output: A Game Class containing key attributes such as:
        - Date, Event, Round
        - White player, Black player
        - Result
        - Missing headers default to None
    Storage: White/Black Elo, Opening are stored in a dictionary but not returned
    """

    headers = game_string.headers

    # Define placeholders that indicate missing info
    empty_values = ["?", "*", "????.??.??", None]

    # The important information get defined
    # and if they don't contain anything, None is returned
    date = headers.get("Date")
    event = headers.get("Event")
    site = headers.get("Site")
    round_num = headers.get("Round")
    white = headers.get("White")
    black = headers.get("Black")
    result = headers.get("Result")

    game_class = Game(date, event, site, round_num, white, black, result)

    if all(h in empty_values for h in [white, black, result]):
        return None

    # All the information that is not considered identity or metadata is stored in dictionary
    # There is currently no use of the following dictionary
    extra_game_info = {
        "White Elo": headers.get("White Elo"),
        "Black Elo": headers.get("Black Elo"),
        "Opening": headers.get("Opening")
        }

    return game_class
