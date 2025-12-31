from src.db.connection_manager import Connection_Manager

def insert_tournament(cursor,game_obj):
    """Ensure each tournament referenced by a Game object exists in the Tournament table."""

    tournament = game_obj.event
    date = game_obj.date

    # ask SQL: does tournament exist? Corresponding to both the name and the date as tournaments
    # can share the same name
    cursor.execute("SELECT Id FROM Tournament WHERE Name = %s;", (tournament,))
    row = cursor.fetchone()

    if row == None:
        cursor.execute("INSERT INTO Tournament (Name) VALUES (%s);", (tournament,))
        tournament_id = cursor.lastrowid

    else:
        # Search for the corresponding ID
        tournament_id = row["Id"]

    return tournament_id