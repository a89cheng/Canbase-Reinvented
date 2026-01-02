from chess.pgn import GameNode

from src.db.connection_manager import Connection_Manager
"""
The cursor is fed into the function in another module
Source: Trust me bro.
"""

#GENERAL ANALYTICS [1]

def total_games(cursor):
    cursor.execute("SELECT COUNT(*) AS games FROM Game;")
    return cursor.fetchone()["games"]

def total_tournaments(cursor):
    cursor.execute("SELECT COUNT(*) AS tournaments FROM Tournament;")
    return cursor.fetchone()["tournaments"]

def average_player_rating(cursor):
    cursor.execute("SELECT AVG(Rating) AS avg_rtng FROM Player;")
    return cursor.fetchone()["avg_rtng"]

def decisive_games(cursor):
    cursor.execute("""
        SELECT COUNT(*) AS decisive_games
        FROM Game
        WHERE Result IN ('1-0', '0-1');
    """)
    return cursor.fetchone()["decisive_games"]

def white_wins(cursor):
    cursor.execute("SELECT COUNT(*) AS white_w FROM Game WHERE Result = '1-0';")
    return cursor.fetchone()["white_w"]

def black_wins(cursor):
    cursor.execute("SELECT COUNT(*) AS black_w FROM Game WHERE Result = '0-1';")
    return cursor.fetchone()["black_w"]

#OPENING ANALYTICS[2]

def top_openings(cursor):
    cursor.execute("""
        SELECT Eco, COUNT(*) AS games_played
        FROM Game
        WHERE Eco IS NOT NULL
        GROUP BY Eco
        ORDER BY games_played DESC;
    """)
    return cursor.fetchall()

def player_openings_all(cursor, player_name):
    cursor.execute("""
        SELECT Eco, COUNT(*) AS games_played
        FROM Game
        JOIN Player
            ON Player.Id = Game.White_player_id
            OR Player.Id = Game.Black_player_id
        WHERE Player.Name = %s
          AND Eco IS NOT NULL
        GROUP BY Eco
        ORDER BY games_played DESC;
    """, (player_name,))
    return cursor.fetchall()

def player_openings_white(cursor, player_name):
    cursor.execute("""
        SELECT Eco, COUNT(*) AS games_played
        FROM Game
        JOIN Player ON Player.Id = Game.White_player_id
        WHERE Player.Name = %s
          AND Eco IS NOT NULL
        GROUP BY Eco
        ORDER BY games_played DESC;
    """, (player_name,))
    return cursor.fetchall()

def player_openings_black(cursor, player_name):
    cursor.execute("""
        SELECT Eco, COUNT(*) AS games_played
        FROM Game
        JOIN Player ON Player.Id = Game.Black_player_id
        WHERE Player.Name = %s
          AND Eco IS NOT NULL
        GROUP BY Eco
        ORDER BY games_played DESC;
    """, (player_name,))
    return cursor.fetchall()

def win_rate_by_opening(cursor, player_name):
    cursor.execute("""
        SELECT 
            Game.Eco, 
            SUM(
                CASE
                    WHEN (Player.Id = Game.White_player_id AND Game.Result = '1-0')
                      OR (Player.Id = Game.Black_player_id AND Game.Result = '0-1')
                    THEN 1 ELSE 0
                END
            ) * 100.0 / COUNT(*) AS Win_Percent
        FROM Player
        INNER JOIN Game 
            ON Player.Id = Game.White_player_id
	        OR Player.Id = Game.Black_player_id
        WHERE Player.Name = %s
        GROUP BY Game.Eco
        ORDER BY Win_Percent DESC;
    """, (player_name,))
    return cursor.fetchall()

#PLAYER ANALYTICS [3]

def players_most_games(cursor):
    cursor.execute("""
        SELECT Id, Name, SUM(games_played) AS total_games
        FROM (
            SELECT Player.Id, Player.Name, COUNT(*) AS games_played
            FROM Player
            JOIN Game ON Player.Id = Game.White_player_id
            GROUP BY Player.Id, Player.Name
            UNION ALL
            SELECT Player.Id, Player.Name, COUNT(*) AS games_played
            FROM Player
            JOIN Game ON Player.Id = Game.Black_player_id
            GROUP BY Player.Id, Player.Name
        ) AS combined
        GROUP BY Id, Name
        ORDER BY total_games DESC;
    """)
    return cursor.fetchall()

def players_highest_winrate(cursor, min_games=10):
    cursor.execute("""
        SELECT Id, Name, SUM(wins) * 100.0/ SUM(games_played) AS win_percentage
        FROM (
            SELECT Player.Id, Player.Name,
                   SUM(CASE WHEN Result = '1-0' THEN 1 ELSE 0 END) AS wins,
                   COUNT(*) AS games_played
            FROM Player
            JOIN Game ON Player.Id = Game.White_player_id
            UNION ALL
            SELECT Player.Id, Player.Name,
                   SUM(CASE WHEN Result = '0-1' THEN 1 ELSE 0 END) AS wins,
                   COUNT(*) AS games_played
            FROM Player
            JOIN Game ON Player.Id = Game.Black_player_id
        ) AS combined
        GROUP BY Id, Name
        HAVING SUM(games_played) >= %s
        ORDER BY win_percentage DESC;
    """, (min_games,))
    return cursor.fetchall()

def player_winrate_by_colour(cursor, player_name):
    cursor.execute("""
    SELECT 
        Player.Id, Player.Name , 
        SUM(
            CASE
                WHEN (Player.Id = Game.White_player_id AND Game.Result = '1-0')
                THEN 1 ELSE 0
            END
        ) * 100.0 / SUM(CASE WHEN Player.Id = Game.White_player_id THEN 1 ELSE 0 END) AS White_Win_Percent,
        SUM(
            CASE
                WHEN (Player.Id = Game.Black_player_id AND Game.Result = '0-1')
                THEN 1 ELSE 0
            END
        ) * 1.0 / SUM(CASE WHEN Player.Id = Game.Black_player_id THEN 1 ELSE 0 END) AS Black_Win_Percent
    FROM Player
    INNER JOIN Game 
        ON Player.Id = Game.White_player_id
        OR Player.Id = Game.Black_player_id
    WHERE Player.Name = %s
    GROUP BY Player.Id, Player.Name; 
    """,(player_name,))
    return cursor.fetchall()

def player_win_loss_draw_and_decisive_game_percent(cursor, player_name):
    cursor.execute("""
        SELECT
            Player.Id, 
            Player.Name,
            SUM(
                CASE
                    WHEN (Player.Id = Game.White_player_id AND Game.Result = '1-0')
                      OR (Player.Id = Game.Black_player_id AND Game.Result = '0-1')
                    THEN 1 ELSE 0
                END
            ) as wins, 
            SUM(
                CASE
                    WHEN (Player.Id = Game.White_player_id AND Game.Result = '0-1')
                      OR (Player.Id = Game.Black_player_id AND Game.Result = '1-0')
                    THEN 1 ELSE 0
                END
            ) as losses,
            SUM(CASE WHEN Game.Result = '1/2-1/2' THEN 1 ELSE 0 END) as draws,
            SUM(
                CASE
                    WHEN (Game.Result = '1-0')
                      OR (Game.Result = '0-1')
                    THEN 1 ELSE 0
                END
            ) *100.0 / COUNT(*) as decisive_percentage
        FROM Player
        INNER JOIN Game 
            ON Player.Id = Game.White_player_id
            OR Player.Id = Game.Black_player_id
        WHERE Player.Name = %s
        GROUP BY Player.Id, Player.Name; 
    """,(player_name,))
    return cursor.fetchall()

#FEDERATION ANALYTICS [4]

def games_by_federation(cursor):
    cursor.execute("""
        SELECT Player.Federation, COUNT(*) AS games
        FROM Player
        JOIN Game
            ON Player.Id = Game.White_player_id
            OR Player.Id = Game.Black_player_id
        GROUP BY Player.Federation
        ORDER BY games DESC;
    """)
    return cursor.fetchall()

def federation_winrate(cursor, min_games=20):
    cursor.execute("""
        SELECT Federation,
               SUM(wins) * 100.0 / SUM(games_played) AS win_percentage
        FROM (
            SELECT Player.Federation,
                   SUM(CASE WHEN Result = '1-0' THEN 1 ELSE 0 END) AS wins,
                   COUNT(*) AS games_played
            FROM Player
            JOIN Game ON Player.Id = Game.White_player_id
            UNION ALL
            SELECT Player.Federation,
                   SUM(CASE WHEN Result = '0-1' THEN 1 ELSE 0 END) AS wins,
                   COUNT(*) AS games_played
            FROM Player
            JOIN Game ON Player.Id = Game.Black_player_id
        ) AS combined
        GROUP BY Federation
        HAVING SUM(games_played) >= %s
        ORDER BY win_percentage DESC;
    """, (min_games,))
    return cursor.fetchall()

#TOURNAMENT ANALYTICS [5]

def games_per_tournament(cursor):
    cursor.execute("""
        SELECT Tournament.Id, Tournament.Name, COUNT(*) AS games
        FROM Tournament
        JOIN Game ON Tournament.Id = Game.Tournament_id
        GROUP BY Tournament.Id, Tournament.Name
        ORDER BY games DESC;
    """)
    return cursor.fetchall()

#NON STATISTICAL QUERIES

def select_all_games(cursor):
    cursor.execute("""
        SELECT White.Name AS 'White' , White.Rating As 'White Elo', Black.Name AS 'Black', Black.Rating AS 'Black Elo' , Game.Result, Game.Moves
        FROM Game
        INNER JOIN Player AS White ON Game.White_player_id = White.Id
        INNER JOIN Player AS Black ON Game.Black_player_id = Black.Id;
    """)
    return cursor.fetchall()

def select_player_all_games(cursor, player_name):
    cursor.execute("""
            SELECT White.Name AS 'White' , White.Rating As 'White Elo', Black.Name AS 'Black', Black.Rating AS 'Black Elo' , Game.Result, Game.Moves
            FROM Game
            INNER JOIN Player AS White ON Game.White_player_id = White.Id
            INNER JOIN Player AS Black ON Game.Black_player_id = Black.Id
            WHERE White.Name = %s OR Black.Name = %s;
        """, (player_name, player_name))
    return cursor.fetchall()

#RESETTING THE PROGRAM
def reset_tables(cursor):
    # Method to reset the table, commit is necessary

    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
    cursor.execute("DROP TABLE IF EXISTS Game;")
    cursor.execute("DROP TABLE IF EXISTS Player;")
    cursor.execute("DROP TABLE IF EXISTS Tournament;")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

    cursor.execute("""
        CREATE TABLE Player (
        Id INTEGER NOT NULL AUTO_INCREMENT,
        Name VARCHAR(50) NOT NULL,
        Rating INTEGER,
        Federation VARCHAR(60),
        PRIMARY KEY (Id)
        );
    """)

    cursor.execute("""
        CREATE TABLE Tournament (
        Id INTEGER NOT NULL AUTO_INCREMENT,
        Name VARCHAR(100) NOT NULL,
        Location VARCHAR(60),
        Start_date DATE,
        Rounds INTEGER,
        PRIMARY KEY (Id)
        );
    """)

    cursor.execute("""
        CREATE TABLE Game (
        Id INTEGER NOT NULL AUTO_INCREMENT ,
        White_player_id INTEGER NOT NULL,
        Black_player_id INTEGER NOT NULL,
        Tournament_id INTEGER NOT NULL,
        Moves VARCHAR(5000),
        Result VARCHAR(7),
        Played_Date VARCHAR(25),
        Eco VARCHAR(50),
        PRIMARY KEY (Id),
        FOREIGN KEY (White_player_id) REFERENCES Player(Id),
        FOREIGN KEY (Black_player_id) REFERENCES Player(Id),
        FOREIGN KEY (Tournament_id) REFERENCES Tournament(Id)
        );
    """)