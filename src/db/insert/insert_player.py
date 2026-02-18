from src.db.connection_manager import Connection_Manager

def insert_players(cursor, game_obj):
    """“Given a Game object, ensure both players exist in the Player table, and return their IDs.”"""

    #Define the 2 players in the game object

    two_players = {game_obj.white : game_obj.white_elo , game_obj.black : game_obj.black_elo}
    ids = []

    #Just so the code iterates twice, once per player
    for person, rating in two_players.items():

        if not person or person.strip().lower() in ["", "?", "unknown"]:
            ids.append(None)
            continue

        # Normalize rating
        if not isinstance(rating, int):
            try:
                rating = int(rating)
            except (TypeError, ValueError):
                rating = None

        # ask SQL: does player exist?
        cursor.execute("SELECT Id FROM Player WHERE Name = %s;", (person,))
        row = cursor.fetchone()


        #If the row corresponding to the player doesn't exist, one is made with an ID
        if row == None:
            cursor.execute("INSERT INTO Player (Name, Rating) VALUES (%s, %s);", (person, rating))
            player_id = cursor.lastrowid

        else:
            # Search for the corresponding ID if it does exist
            player_id = row["Id"]

            if rating:
                cursor.execute("""
                            UPDATE Player
                            SET Rating = %s
                            WHERE Id = %s;
                            """, (rating, player_id))

        #ID is appended and extracted
        ids.append(player_id)

    #By the end, there should either be a returned Id, or a created and returned Id!
    white_id , black_id = ids[0] , ids[1]

    #Values of white Id, black Id returned
    return white_id , black_id