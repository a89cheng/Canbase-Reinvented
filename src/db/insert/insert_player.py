from src.db.connection import create_db_connection

def insert_players(game_obj):
    """“Given a Game object, ensure both players exist in the Player table, and return their IDs.”"""

    #Creating the connection object
    connection = create_db_connection("localhost", "root", "2r546482ek83exm4", "Canbase_Reinvented")
    cursor = connection.cursor()

    #Define the 2 players in the game object
    white_player = game_obj.white
    black_player = game_obj.black
    ids = []

    #Just so the code iterates twice, once per player
    for person in [white_player ,  black_player]:
        # ask SQL: does player exist?
        cursor.execute("SELECT Id FROM Player WHERE Name = %s;", (person,))
        row = cursor.fetchone()

        #If the row corresponding to the player doesn't exist, one is made with an ID
        if row == None:
            cursor.execute("INSERT INTO Player (Name) VALUES (%s);", (person,))
            connection.commit()
            player_id = cursor.lastrowid

        else:
            # Search for the corresponding ID if it does exist
            player_id = row[0]

        if person.strip().lower() in ["", "?", "unknown"]:
            player_id = None
        #ID is appended and extracted
        ids.append(player_id)

    # Close both the cursor and the database connection accordingly
    cursor.close()
    connection.close()

    #By the end, there should either be a returned Id, or a created and returned Id!
    white_id , black_id= ids[0] , ids[1]

    #Values of white Id, black Id returned
    return white_id , black_id