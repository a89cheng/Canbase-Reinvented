from src.db.connection import create_db_connection

def insert_tournament(game_obj):
    """“Ensure each tournament referenced by a Game object exists in the Tournament table."""

    #Creating the connection object
    connection = create_db_connection("localhost", "root", "password here", "Canbase_Reinvented")
    cursor = connection.cursor()

    tournament = game_obj.event
    date = game_obj.date

    # ask SQL: does tournament exist? Corresponding to both the name and the date as tournaments
    # can share the same name
    cursor.execute("SELECT Id FROM Tournament WHERE Name = %s AND Start_date = %s;", (tournament, date))
    row = cursor.fetchone()

    if row == None:
        cursor.execute("INSERT INTO Tournament (Name, Start_date) VALUES (%s, %s);", (tournament,date))
        connection.commit()
        tournament_id = cursor.lastrowid

    else:
        # Search for the corresponding ID
        tournament_id = row[0]

    # Close both the cursor and the database connection accordingly
    cursor.close()
    connection.close()

    return tournament_id