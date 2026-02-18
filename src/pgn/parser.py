import io , os
import chess , chess.pgn
from src.models.game import Game

def convert_pgn_file(pgn_path_or_file):
    """
    Convert a PGN file OR PGN path into a file-like text object suitable for parsing.
    Input: pgn_path: string path to PGN file OR pgn_file: a binary file object containing PGN data.
    Output: A StringIO object containing the decoded text from the PGN file,
            which can be read sequentially by the parser.
    """
    if isinstance(pgn_path_or_file , (str, os.PathLike)):
        pgn_path = pgn_path_or_file
        with open(pgn_path, "rb") as file:  # open binary
            text = file.read().decode("utf-8")
            pgn_text = io.StringIO(text)

    elif hasattr(pgn_path_or_file, "read"):
        pgn_file = pgn_path_or_file
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

        # Games are added to the game list after being transformed into a game object
        games.append(parse_game(game))

    #Returns list of Game objects
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
    white_elo = headers.get("White Elo")
    black = headers.get("Black")
    black_elo = headers.get("Black Elo")
    result = headers.get("Result")
    eco = headers.get("ECO")
    moves = extract_moves_string(game_string)

    game_class = Game(date, event, site, round_num, white, white_elo, black, black_elo, result, eco, moves)


    return game_class

def extract_moves_string(game_obj):
    """
    Convert a python-chess Game object into a PGN-style string with turn numbers.
    Input: game_obj: python-chess Game object
    Output: String of moves like "1. e4 e5 2. Nf3 Nc6 3. Bb5 a6"
    """

    board = game_obj.board()
    moves_list = []
    turn = 1
    is_white = True
    turn_str = ""

    for move in game_obj.mainline_moves():
        san = board.san(move)
        #The board is updated with the previous move
        board.push(move)

        if is_white:
            # start a new turn entry
            turn_str = f"{turn}. {san}"
            is_white = False
        else:
            # append black move to the turn
            turn_str += f" {san}"
            moves_list.append(turn_str)
            turn += 1
            is_white = True

    # if game ends on a white move only, add that last turn
    if not is_white:
        moves_list.append(turn_str)

    return " ".join(moves_list)
