from src.db.connection import create_db_connection

def insert_game(game_obj):
    """Insert individual games into the Game table."""

    #Creating the connection object
    connection = create_db_connection("localhost", "root", "password here", "Canbase_Reinvented")
    cursor = connection.cursor()

    #Define the 2 players in the game object
    cursor.execute("SELECT Id FROM Player WHERE Name = %s;", (game_obj.white,))
    white_id = cursor.fetchone()[0]
    cursor.execute("SELECT Id FROM Player WHERE Name = %s;", (game_obj.black,))
    black_id = cursor.fetchone()[0]
    cursor.execute("SELECT Id FROM Tournament WHERE Name = %s AND Start_date = %s;", (game_obj.event, game_obj.date))
    tournament_id = cursor.fetchone()[0]
    result = game_obj.result
    eco = game_obj.eco
    moves = game_obj.moves
    date = game_obj.date

    cursor.execute("INSERT INTO Game (White_player_id , Black_player_id , Tournament_id , Result, Eco, Moves, Played_Date) "
                   "VALUES (%s,%s,%s,%s,%s,%s,%s);", (white_id , black_id , tournament_id , result, eco, moves, date)
    )
    connection.commit()

    game_id = cursor.lastrowid

    # Close both the cursor and the database connection accordingly
    cursor.close()
    connection.close()

    return game_id