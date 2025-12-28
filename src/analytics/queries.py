from src.db.connection_manager import Connection_Manager
"""
The cursor is fed into the function in another module
Source: Trust me bro.
"""

#GENERAL ANALYTICS [1]

def total_games(cursor):
    cursor.execute("SELECT COUNT(*) FROM Game;")
    return cursor.fetchone()[0]

def total_tournaments(cursor):
    cursor.execute("SELECT COUNT(*) FROM Tournament;")
    return cursor.fetchone()[0]

def average_player_rating(cursor):
    cursor.execute("SELECT AVG(Rating) FROM Player;")
    return cursor.fetchone()[0]

def decisive_games(cursor):
    cursor.execute("""
        SELECT COUNT(*)
        FROM Game
        WHERE Result IN ('1-0', '0-1');
    """)
    return cursor.fetchone()[0]

def white_wins(cursor):
    cursor.execute("SELECT COUNT(*) FROM Game WHERE Result = '1-0';")
    return cursor.fetchone()[0]

def black_wins(cursor):
    cursor.execute("SELECT COUNT(*) FROM Game WHERE Result = '0-1';")
    return cursor.fetchone()[0]

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
            ) * 1.0 / COUNT(*) AS Win_Percent
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
        SELECT Id, Name, SUM(wins) * 1.0 / SUM(games_played) AS win_percentage
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
        ) * 1.0 / SUM(CASE WHEN Player.Id = Game.White_player_id THEN 1 ELSE 0 END) AS White_Win_Percent,
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
            ) *1.0 / COUNT(*) as decisive_percentage
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
               SUM(wins) * 1.0 / SUM(games_played) AS win_percentage
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