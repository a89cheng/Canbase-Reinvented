from src.db.connection import create_db_connection
from datetime import datetime

def report_error(game_obj , error_message):
    """The report error function logs a game insertion error into insert_errors"""
    # Format: 2025-12-22 16:55:12 | Failed to insert game | White=Carlsen | Black=Nepo | Event=WCC 2023 | Error=Player not found

    #Method used to get the date and time
    date_time = timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_line = (f"{date_time} | Failed to insert game |"
                f"White={game_obj.white} | Black={game_obj.black} | Event={game_obj.event}"
                f"Error={error_message}")

    #a(append) used instead of w(write) as not to erase old logs
    with open("insert_errors.log", "a") as infile:
        infile.write(log_line)


def insert_game(game_obj):
    """Insert individual games into the Game table."""

    #Creating the connection object
    connection = create_db_connection("localhost", "root", "password here", "Canbase_Reinvented")
    cursor = connection.cursor()

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

    result = game_obj.result
    eco = game_obj.eco
    moves = game_obj.moves
    date = game_obj.date

    try:
        cursor.execute("INSERT INTO Game (White_player_id , Black_player_id , Tournament_id , Result, Eco, Moves, Played_Date) "
                       "VALUES (%s,%s,%s,%s,%s,%s,%s);", (white_id , black_id , tournament_id , result, eco, moves, date)
        )
    except Exception as e:
        report_error(game_obj , error_message=str(e))
        cursor.close()
        connection.close()
        return None

    connection.commit()

    game_id = cursor.lastrowid

    # Close both the cursor and the database connection accordingly
    cursor.close()
    connection.close()

    return game_id