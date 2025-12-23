from src.db.connection import create_db_connection
#Not entirely sure where I'm importing from... but god to know
from datetime import datetime

"""
Testing Notes: From using the pytest testing of the insertions, the connection has to be refreshed 
on the outside of the function call in order for the change to be viewed on the table {12/23/2025}
- Later implementation of a Connection Class should solve the problem! 
"""


def report_error(game_obj , error_message):
    """The report error function logs a game insertion error into insert_errors"""
    # Format: 2025-12-22 16:55:12 | Failed to insert game | White=Carlsen | Black=Nepo | Event=WCC 2023 | Error=Player not found

    #Method used to get the date and time from the datetime library...
    #Would assume strftime is the format of the date
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    #This is the organized sting that will be written / appended to the log
    log_line = (f"{date_time} | Failed to insert game |"
                f"White={game_obj.white} | Black={game_obj.black} | Event={game_obj.event} |"
                f"Error={type(error_message).__name__}: {error_message}\n")

    #a(append) used instead of w(write) as not to erase old logs
    with open("insert_errors.log", "a") as infile:
        infile.write(log_line)


def insert_game(game_obj, white_id, black_id, tourney_id):
    """Insert individual games into the Game table."""

    #Creating the connection object
    connection = create_db_connection("localhost", "root", "password", "Canbase_Reinvented")
    cursor = connection.cursor()

    """
    #Define the 2 players in the game object
    cursor.execute("SELECT Id FROM Player WHERE Name = %s;", (game_obj.white,))
    row = cursor.fetchone()
    if row is None:
        raise ValueError("Player not found")
    white_id = row[0]

    cursor.execute("SELECT Id FROM Player WHERE Name = %s;", (game_obj.black,))
    row = cursor.fetchone()
    if row is None:
        raise ValueError("Player not found")
    black_id = row[0]

    cursor.execute("SELECT Id FROM Tournament WHERE Name = %s;", (game_obj.event,))
    row = cursor.fetchone()
    if row is None:
        raise ValueError("Tournament not found")
    tournament_id = row[0]
    """

    #Other required definitions
    result = game_obj.result
    eco = game_obj.eco
    moves = game_obj.moves
    date = game_obj.date

    #If any of the code core Ids return as None, then an error is raised
    if None in [white_id, black_id, tourney_id]:
        raise ValueError("Cannot insert game: one or more IDs are missing")

    #Placedin try block in case the insert fails...
    try:
        cursor.execute("INSERT INTO Game (White_player_id , Black_player_id , Tournament_id , Result, Eco, Moves, Played_Date) "
                       "VALUES (%s,%s,%s,%s,%s,%s,%s);", (white_id , black_id , tourney_id , result, eco, moves, date)
        )
    #Whatever exception as e... standard python syntax
    except Exception as e:
        #Error message is a textbook python variable?
        report_error(game_obj , error_message=str(e))
        cursor.close()
        connection.close()
        return None
    else:
        connection.commit()

    game_id = cursor.lastrowid

    # Close both the cursor and the database connection accordingly
    cursor.close()
    connection.close()

    return game_id