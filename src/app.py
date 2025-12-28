import streamlit as st
from src.db.connection_manager import Connection_Manager
from data.bulk_insert import bulk_insert
#Grouping the imports by the type of analytic regardless of where it is from
from src.analytics.queries import (
    total_games, total_tournaments, average_player_rating,
    decisive_games, white_wins, black_wins
)
from src.analytics.queries import (
    player_openings_all, player_openings_white, player_openings_black,
    win_rate_by_opening, player_winrate_by_colour, player_win_loss_draw_and_decisive_game_percent
)

# Initialize connection manager object
conn_manager = Connection_Manager()

# --- 1. File upload or path input ---
st.title("Canbase Reinvented Analytics")

uploaded_file = st.file_uploader("Upload a PGN file", type="pgn")
file_path_input = st.text_input("Or type the path to a PGN file:")

if uploaded_file or file_path_input:
    # Here you would call your insert functions to populate the DB
    st.write("File received. Parsing and inserting into DB...")
    if uploaded_file:
        conn_manager.handle_SQL(
            bulk_insert,
            commit = True,
            file = uploaded_file,
        )
    else:
        conn_manager.handle_SQL(
            bulk_insert,
            commit = True,
            file_path = file_path_input
        )

# --- 2. General Analytics ---
st.header("General Analytics")
if st.button("Generate General Analytics"):
    # Each of these calls your backend analytics functions through handle_SQL
    total = conn_manager.handle_SQL(total_games)
    tournaments = conn_manager.handle_SQL(total_tournaments)
    avg_rating = conn_manager.handle_SQL(average_player_rating)
    decisive = conn_manager.handle_SQL(decisive_games)
    white = conn_manager.handle_SQL(white_wins)
    black = conn_manager.handle_SQL(black_wins)

    # Display results
    st.write(f"Total games: {total}")
    st.write(f"Total tournaments: {tournaments}")
    st.write(f"Average player rating: {avg_rating}")
    st.write(f"Decisive games: {decisive}")
    st.write(f"White wins: {white}")
    st.write(f"Black wins: {black}")

# --- 3. Player-specific Analytics ---
st.header("Player Analytics")
player_name = st.text_input("Enter player name for specific analytics:")

if st.button("Generate Player Analytics") and player_name:
    st.write(f"Analytics for {player_name}:")
    # Example: pass player_name via kwargs in handle_SQL
    openings = conn_manager.handle_SQL(player_openings_all, player_name=player_name)
    white_openings = conn_manager.handle_SQL(player_openings_white, player_name=player_name)
    black_openings = conn_manager.handle_SQL(player_openings_black, player_name=player_name)
    win_by_opening = conn_manager.handle_SQL(win_rate_by_opening, player_name=player_name)
    winrate_colour = conn_manager.handle_SQL(player_winrate_by_colour, player_name=player_name)
    win_loss_draw = conn_manager.handle_SQL(player_win_loss_draw_and_decisive_game_percent, player_name=player_name)

    # Display results (tables, text, or charts)
    st.write("Top Openings (All):", openings)
    st.write("Top Openings (White):", white_openings)
    st.write("Top Openings (Black):", black_openings)
    st.write("Win Rate by Opening:", win_by_opening)
    st.write("Winrate by Colour:", winrate_colour)
    st.write("Win/Loss/Draw and Decisive %:", win_loss_draw)

# --- 4. Refresh / Reset ---
if st.button("Refresh Page"):
    st.experimental_rerun()

"""
OLD CODE
from src.db.Connection_Manager import create_db_connection
from analytics.queries import total_games, top_openings

def main():
    conn = create_db_connection(1,2,3,4)

    print("Total games:", total_games(conn))

    for row in top_openings(conn)[:5]:
        print(row)

    conn.close()

    # Check if it’s closed
    if not conn.is_connected():
        print("Connection successfully closed.")
    else:
        print("Connection is still open!")

if __name__ == "__main__":
    main()
"""
