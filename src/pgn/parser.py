import io
import chess
import chess.pgn

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
    Output: A dictionary containing key attributes such as:
        - Date, Event, Round
        - White player, White Elo, Black player, Black Elo
        - Result, Opening
        - Missing headers default to "Unknown".
    """

    #Each index represents one game...

    headers = game_string.headers

    game_info = {
        "Date": headers.get("Date" , "Unknown"),
        "Event": headers.get("Event", "Unknown"),
        "Site": headers.get("Site", "Unknown"),
        "Round": headers.get("Round", "Unknown"),

        "White": headers.get("White", "Unknown"),
        "White Elo": headers.get("White Elo", "Unknown"),
        "Black": headers.get("Black", "Unknown"),
        "Black Elo": headers.get("Black Elo", "Unknown"),

        "Result": headers.get("Result", "Unknown"),
        "Opening": headers.get("Opening", "Unknown"),
        }

    return game_info
