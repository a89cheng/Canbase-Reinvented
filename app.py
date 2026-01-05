"""Run with: streamlit run app.py"""
"""(venv ) ricechessmaster@eduroam-campus-10-36-29-147 Canbase Reinvented % /Users/ricechessmaster/Downloads/lichess_db_standard_rated_2019-06.pgn"""

import streamlit as st
import pandas as pd
from src.db.connection_manager import Connection_Manager
from data.bulk_insert import bulk_insert
from src.analytics.utility import Eco_to_opening
# Grouping analytics imports by type
from src.analytics.queries import (
    total_games, total_tournaments, average_player_rating,
    decisive_games, white_wins, black_wins , reset_tables,
    select_all_games , select_player_all_games
)
from src.analytics.queries import (
    player_openings_all, player_openings_white, player_openings_black,
    win_rate_by_opening, player_winrate_by_colour, player_win_loss_draw_and_decisive_game_percent
)


def main():
    # ---------------------------
    # SESSION STATE INITIALIZATION
    # ---------------------------
    # Prevents the same PGN data from being inserted multiple times per session
    if "data_inserted" not in st.session_state:
        st.session_state.data_inserted = False

    # ---------------------------
    # CONNECTION MANAGER
    # ---------------------------
    # Handles DB interactions; used for all analytics queries
    conn_manager = Connection_Manager()

    # ---------------------------
    # SIDEBAR: PGN INPUT & PLAYER SELECTION
    # ---------------------------
    with st.sidebar:
        st.title("PGN Input & Player Analytics")

        # File uploader widget for PGN files
        uploaded_file = st.file_uploader("Upload a PGN file", type="pgn")

        # Optional manual path input for a PGN file
        file_path_input = st.text_input("Or type the path to a PGN file:")

        # Player name input for player-specific analytics
        player_name = st.text_input("Player name for analytics:")

        # Insert PGN into DB only if not already inserted this session
        can_insert = uploaded_file or file_path_input

        if can_insert and not st.session_state.data_inserted:

            conn_manager.handle_SQL(reset_tables, commit=True)

            if st.button("Insert PGN into Database"):
                st.write("Parsing and inserting into DB...")
                if uploaded_file:
                    conn_manager.handle_SQL(bulk_insert, commit=True, pgn_file=uploaded_file)
                else:
                    conn_manager.handle_SQL(bulk_insert, commit=True, pgn_file=file_path_input)

                st.session_state.data_inserted = True
                st.success("Insertion complete.")
        elif st.session_state.data_inserted:
            st.info("Data already inserted this session. Refresh page to insert a new PGN.")

    # ---------------------------
    # MAIN PAGE TITLE
    # ---------------------------
    st.title("Chess Analytics Dashboard [Canbase+]")

    # ---------------------------
    # GENERAL ANALYTICS SECTION
    # ---------------------------
    with st.expander("General Analytics", expanded=True):
        # Trigger analytics only on button click to avoid auto-refresh overhead
        if st.button("Generate General Analytics"):
            # Call backend analytics functions via connection manager
            total = conn_manager.handle_SQL(total_games)
            tournaments = conn_manager.handle_SQL(total_tournaments)
            avg_rating = conn_manager.handle_SQL(average_player_rating)
            decisive = conn_manager.handle_SQL(decisive_games)
            white = conn_manager.handle_SQL(white_wins)
            black = conn_manager.handle_SQL(black_wins)

            all_games = pd.DataFrame(conn_manager.handle_SQL(select_all_games))
            st.dataframe(all_games)

            # Display results as text
            st.write(f"Total games: {total}")
            st.write(f"Total tournaments: {tournaments}")
            st.write(f"Average player rating: {avg_rating}")
            st.write(f"Decisive games: {decisive}")
            st.write(f"White wins: {white}")
            st.write(f"Black wins: {black}")

    # ---------------------------
    # PLAYER-SPECIFIC ANALYTICS SECTION
    # ---------------------------
    with st.expander("Player Analytics", expanded=True):
        # Create the button first, give it a unique key
        generate_player_btn = st.button("Generate Player Analytics", key="player_analytics_btn")

        # Only process analytics if button clicked
        if generate_player_btn:
            # Check if player_name input is filled
            if not player_name:
                st.warning("Please enter a player name to generate analytics.")
            else:
                st.write(f"Analytics for {player_name}:")

                # Call backend queries for this player
                openings = pd.DataFrame(conn_manager.handle_SQL(player_openings_all, player_name=player_name))
                white_openings = pd.DataFrame(conn_manager.handle_SQL(player_openings_white, player_name=player_name))
                black_openings = pd.DataFrame(conn_manager.handle_SQL(player_openings_black, player_name=player_name))
                win_by_opening = pd.DataFrame(conn_manager.handle_SQL(win_rate_by_opening, player_name=player_name))

                # Convert ECO codes to opening names
                openings["opening_name"] = openings["Eco"].apply(Eco_to_opening)
                white_openings["opening_name"] = white_openings["Eco"].apply(Eco_to_opening)
                black_openings["opening_name"] = black_openings["Eco"].apply(Eco_to_opening)
                win_by_opening["opening_name"] = win_by_opening["Eco"].apply(Eco_to_opening)

                winrate_colour = pd.DataFrame(conn_manager.handle_SQL(player_winrate_by_colour, player_name=player_name))
                win_loss_draw = pd.DataFrame(conn_manager.handle_SQL(player_win_loss_draw_and_decisive_game_percent, player_name=player_name))

                # Display analytics results
                st.subheader("Top Openings (All)")
                st.dataframe(openings)

                st.subheader("Top Openings (White):")
                st.dataframe(white_openings)

                st.subheader("Top Openings (Black):")
                st.dataframe(black_openings)

                st.subheader("Win Rate by Opening")
                st.dataframe(win_by_opening)

                st.subheader("Winrate by Colour")
                st.dataframe(winrate_colour)

                st.subheader("Win/Loss/Draw and Decisive %:")
                st.dataframe(win_loss_draw)

                # Display all games for the player
                players_games = pd.DataFrame(
                    conn_manager.handle_SQL(select_player_all_games, player_name=player_name)
                )
                st.dataframe(players_games)

if __name__ == "__main__":
    main()