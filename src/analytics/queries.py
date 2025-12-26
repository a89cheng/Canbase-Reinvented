"""
The connection is fed into the function in another module
Source: Trust me bro.
"""

#GENERAL ANALYTICS [1]

def total_games(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Game;")
    result = cursor.fetchone()[0]
    cursor.close()
    return result


def total_tournaments(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Tournament;")
    result = cursor.fetchone()[0]
    cursor.close()
    return result


def average_player_rating(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT AVG(Rating) FROM Player;")
    result = cursor.fetchone()[0]
    cursor.close()
    return result


def decisive_games(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*)
        FROM Game
        WHERE Result IN ('1-0', '0-1');
    """)
    result = cursor.fetchone()[0]
    cursor.close()
    return result


def white_wins(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Game WHERE Result = '1-0';")
    result = cursor.fetchone()[0]
    cursor.close()
    return result


def black_wins(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Game WHERE Result = '0-1';")
    result = cursor.fetchone()[0]
    cursor.close()
    return result

#OPENING ANALYTICS[2]

def top_openings(conn):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT Eco, COUNT(*) AS games_played
        FROM Game
        WHERE Eco IS NOT NULL
        GROUP BY Eco
        ORDER BY games_played DESC;
    """)
    results = cursor.fetchall()
    cursor.close()
    return results


def player_openings_all(conn, player_name):
    cursor = conn.cursor(dictionary=True)
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
    results = cursor.fetchall()
    cursor.close()
    return results


def player_openings_white(conn, player_name):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT Eco, COUNT(*) AS games_played
        FROM Game
        JOIN Player ON Player.Id = Game.White_player_id
        WHERE Player.Name = %s
          AND Eco IS NOT NULL
        GROUP BY Eco
        ORDER BY games_played DESC;
    """, (player_name,))
    results = cursor.fetchall()
    cursor.close()
    return results


def player_openings_black(conn, player_name):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT Eco, COUNT(*) AS games_played
        FROM Game
        JOIN Player ON Player.Id = Game.Black_player_id
        WHERE Player.Name = %s
          AND Eco IS NOT NULL
        GROUP BY Eco
        ORDER BY games_played DESC;
    """, (player_name,))
    results = cursor.fetchall()
    cursor.close()
    return results

#PLAYER ANALYICS [3]

def players_most_games(conn):
    cursor = conn.cursor(dictionary=True)
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
    results = cursor.fetchall()
    cursor.close()
    return results


def players_highest_winrate(conn, min_games=10):
    cursor = conn.cursor(dictionary=True)
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
    results = cursor.fetchall()
    cursor.close()
    return results

#FEDERATION AALYTICS [4]

def games_by_federation(conn):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT Player.Federation, COUNT(*) AS games
        FROM Player
        JOIN Game
            ON Player.Id = Game.White_player_id
            OR Player.Id = Game.Black_player_id
        GROUP BY Player.Federation
        ORDER BY games DESC;
    """)
    results = cursor.fetchall()
    cursor.close()
    return results


def federation_winrate(conn, min_games=20):
    cursor = conn.cursor(dictionary=True)
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
    results = cursor.fetchall()
    cursor.close()
    return results

#TOURNAMENT ANALYTICS [5]

def games_per_tournament(conn):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT Tournament.Id, Tournament.Name, COUNT(*) AS games
        FROM Tournament
        JOIN Game ON Tournament.Id = Game.Tournament_id
        GROUP BY Tournament.Id, Tournament.Name
        ORDER BY games DESC;
    """)
    results = cursor.fetchall()
    cursor.close()
    return results
