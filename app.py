#Run with: streamlit run app.py

import streamlit as st
import pandas as pd
from src.db.connection_manager import Connection_Manager
from data.bulk_insert import bulk_insert
from src.analytics.utility import Eco_to_opening
from src.analytics.queries import (
    total_games, total_tournaments, average_player_rating,
    decisive_games, white_wins, black_wins, reset_tables,
    select_all_games, select_player_all_games
)
from src.analytics.queries import (
    player_openings_all, player_openings_white, player_openings_black,
    win_rate_by_opening, player_winrate_by_colour, player_win_loss_draw_and_decisive_game_percent
)

# ---------------------------
# PAGE CONFIG & GLOBAL STYLES
# ---------------------------
st.set_page_config(
    page_title="Canbase+ Chess Analytics",
    page_icon="♟️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@300;400;500&display=swap');

/* ── Root palette ── */
:root {
    --bg:        #0d0d0d;
    --surface:   #161616;
    --surface2:  #1e1e1e;
    --border:    #2a2a2a;
    --gold:      #c0392b;
    --gold-dim:  #7b241c;
    --ivory:     #f5f0f0;
    --muted:     #7a7a7a;
    --white-win: #e8e8e8;
    --black-win: #4a9eff;
    --draw:      #c0392b;
}

/* ── Global reset ── */
html, body, .stApp {
    background-color: var(--bg) !important;
    color: var(--ivory) !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 4rem !important; max-width: 1300px; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] * { color: var(--ivory) !important; }
[data-testid="stSidebar"] .stTextInput > div > div > input,
[data-testid="stSidebar"] .stFileUploader label {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    color: var(--ivory) !important;
    border-radius: 4px;
}

/* Sidebar title */
[data-testid="stSidebar"] h1 {
    font-family: 'Playfair Display', serif !important;
    font-size: 1.3rem !important;
    color: var(--gold) !important;
    letter-spacing: 0.03em;
    border-bottom: 1px solid var(--gold-dim);
    padding-bottom: 0.6rem;
    margin-bottom: 1.2rem !important;
}

/* ── Main title ── */
h1 {
    font-family: 'Playfair Display', serif !important;
    font-size: 2.8rem !important;
    font-weight: 900 !important;
    color: var(--ivory) !important;
    letter-spacing: -0.01em;
    line-height: 1.1 !important;
}
h1 span.accent { color: var(--gold); }

/* ── Section headings ── */
h2, h3, .stExpander summary p {
    font-family: 'Playfair Display', serif !important;
    color: var(--gold) !important;
    letter-spacing: 0.02em;
}
h3 { font-size: 1rem !important; text-transform: uppercase; letter-spacing: 0.12em; }

/* ── Expanders ── */
.stExpander {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    margin-bottom: 1.2rem !important;
}
.stExpander summary {
    background: var(--surface2) !important;
    border-radius: 6px 6px 0 0 !important;
    padding: 0.8rem 1.2rem !important;
}
.stExpander summary:hover { background: #222 !important; }

/* ── Buttons ── */
.stButton > button {
    background: transparent !important;
    border: 1px solid var(--gold) !important;
    color: var(--gold) !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 0.5rem 1.4rem !important;
    border-radius: 2px !important;
    transition: all 0.2s ease;
}
.stButton > button:hover {
    background: var(--gold) !important;
    color: var(--bg) !important;
}

/* ── Metric cards ── */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 1rem;
    margin: 1.2rem 0;
}
.metric-card {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-top: 2px solid var(--gold);
    border-radius: 4px;
    padding: 1rem 1.2rem;
}
.metric-card .label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--muted);
    margin-bottom: 0.3rem;
}
.metric-card .value {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--ivory);
    line-height: 1;
}
.metric-card .value.red { color: var(--gold); }

/* ── Dataframes ── */
.stDataFrame {
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
    overflow: hidden;
}
[data-testid="stDataFrame"] table {
    background: var(--surface2) !important;
    color: var(--ivory) !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.8rem !important;
}
[data-testid="stDataFrame"] thead tr th {
    background: var(--surface) !important;
    color: var(--gold) !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.7rem !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    border-bottom: 1px solid var(--gold-dim) !important;
}
[data-testid="stDataFrame"] tbody tr:hover td {
    background: #222 !important;
}

/* ── Info / warning / success ── */
.stAlert {
    background: var(--surface2) !important;
    border-left: 3px solid var(--gold) !important;
    color: var(--ivory) !important;
    border-radius: 4px !important;
}

/* ── Divider ── */
.chess-divider {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: 1.6rem 0 1.2rem;
}
.chess-divider span.label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: var(--gold);
    white-space: nowrap;
}
.chess-divider .line {
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ── Section tag badge ── */
.section-tag {
    display: inline-block;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: var(--bg);
    background: var(--gold);
    padding: 0.2rem 0.6rem;
    border-radius: 2px;
    margin-bottom: 0.5rem;
}

/* ── Board pattern watermark ── */
.board-watermark {
    position: fixed;
    top: 0; right: 0;
    width: 340px; height: 340px;
    opacity: 0.025;
    pointer-events: none;
    background-image:
        repeating-conic-gradient(#fff 0% 25%, transparent 0% 50%);
    background-size: 42px 42px;
    z-index: 0;
}
</style>

<div class="board-watermark"></div>
""", unsafe_allow_html=True)


def section_divider(label):
    st.markdown(f"""
    <div class="chess-divider">
        <div class="line"></div>
        <span class="label">♟ {label}</span>
        <div class="line"></div>
    </div>
    """, unsafe_allow_html=True)


def main():
    # ---------------------------
    # SESSION STATE
    # ---------------------------
    if "data_inserted" not in st.session_state:
        st.session_state.data_inserted = False

    conn_manager = Connection_Manager()

    # ---------------------------
    # SIDEBAR
    # ---------------------------
    with st.sidebar:
        st.markdown("# Canbase+")
        st.markdown('<div class="section-tag">Import</div>', unsafe_allow_html=True)

        uploaded_file = st.file_uploader("Upload a PGN file", type="pgn")
        file_path_input = st.text_input("Or paste a file path:")
        player_name = st.text_input("Player name for analytics:")

        can_insert = uploaded_file or file_path_input
        if can_insert and not st.session_state.data_inserted:
            conn_manager.handle_SQL(reset_tables, commit=True)
            if st.button("⬆ Insert PGN into Database"):
                with st.spinner("Parsing & inserting…"):
                    if uploaded_file:
                        conn_manager.handle_SQL(bulk_insert, commit=True, pgn_file=uploaded_file)
                    else:
                        conn_manager.handle_SQL(bulk_insert, commit=True, pgn_file=file_path_input)
                st.session_state.data_inserted = True
                st.success("Insertion complete.")
        elif st.session_state.data_inserted:
            st.info("Data loaded this session. Refresh to import a new PGN.")

    # ---------------------------
    # HEADER
    # ---------------------------
    st.markdown("""
    <h1>Chess Analytics <span class="accent">Dashboard</span></h1>
    <p style="font-family:'IBM Plex Mono',monospace;font-size:0.75rem;color:#7a7a7a;letter-spacing:0.12em;text-transform:uppercase;margin-top:-0.5rem;margin-bottom:2rem;">
        Canbase+ &nbsp;·&nbsp; Lichess PGN Explorer
    </p>
    """, unsafe_allow_html=True)

    # ---------------------------
    # GENERAL ANALYTICS
    # ---------------------------
    with st.expander("♜  General Analytics", expanded=True):
        if st.button("Generate General Analytics", key="gen_analytics"):
            total     = conn_manager.handle_SQL(total_games)
            tournaments = conn_manager.handle_SQL(total_tournaments)
            avg_rating  = conn_manager.handle_SQL(average_player_rating)
            decisive    = conn_manager.handle_SQL(decisive_games)
            white       = conn_manager.handle_SQL(white_wins)
            black       = conn_manager.handle_SQL(black_wins)

            # Metric cards row
            st.markdown(f"""
            <div class="metric-grid">
                <div class="metric-card">
                    <div class="label">Total Games</div>
                    <div class="value red">{total}</div>
                </div>
                <div class="metric-card">
                    <div class="label">Tournaments</div>
                    <div class="value">{tournaments}</div>
                </div>
                <div class="metric-card">
                    <div class="label">Avg. Rating</div>
                    <div class="value">{avg_rating if avg_rating is not None else "—"}</div>
                </div>
                <div class="metric-card">
                    <div class="label">Decisive Games</div>
                    <div class="value">{decisive}</div>
                </div>
                <div class="metric-card">
                    <div class="label">White Wins</div>
                    <div class="value">{white}</div>
                </div>
                <div class="metric-card">
                    <div class="label">Black Wins</div>
                    <div class="value">{black}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            section_divider("All Games")
            all_games = pd.DataFrame(conn_manager.handle_SQL(select_all_games))
            st.dataframe(all_games, use_container_width=True)

    # ---------------------------
    # PLAYER ANALYTICS
    # ---------------------------
    with st.expander("♛  Player Analytics", expanded=True):
        if st.button("Generate Player Analytics", key="player_analytics_btn"):
            if not player_name:
                st.warning("Enter a player name in the sidebar first.")
            else:
                st.markdown(f"""
                <div style="margin:0.8rem 0 1.4rem;display:flex;align-items:center;gap:1rem;">
                    <span style="font-family:'IBM Plex Mono',monospace;font-size:0.6rem;
                                 text-transform:uppercase;letter-spacing:0.15em;color:#0d0d0d;
                                 background:#c0392b;padding:0.25rem 0.7rem;border-radius:2px;">Player</span>
                    <span style="font-family:'Playfair Display',serif;font-size:1.8rem;font-weight:700;
                                 color:#f5f0f0;line-height:1;">{player_name}</span>
                </div>
                """, unsafe_allow_html=True)

                openings       = pd.DataFrame(conn_manager.handle_SQL(player_openings_all,   player_name=player_name))
                white_openings = pd.DataFrame(conn_manager.handle_SQL(player_openings_white, player_name=player_name))
                black_openings = pd.DataFrame(conn_manager.handle_SQL(player_openings_black, player_name=player_name))
                win_by_opening = pd.DataFrame(conn_manager.handle_SQL(win_rate_by_opening,   player_name=player_name))

                if openings.empty:
                    st.warning("Player not found. Please try another name.")
                    st.stop()

                openings["opening_name"]       = openings["Eco"].apply(Eco_to_opening)
                white_openings["opening_name"] = white_openings["Eco"].apply(Eco_to_opening)
                black_openings["opening_name"] = black_openings["Eco"].apply(Eco_to_opening)
                win_by_opening["opening_name"] = win_by_opening["Eco"].apply(Eco_to_opening)

                winrate_colour = pd.DataFrame(conn_manager.handle_SQL(player_winrate_by_colour, player_name=player_name))
                win_loss_draw  = pd.DataFrame(conn_manager.handle_SQL(player_win_loss_draw_and_decisive_game_percent, player_name=player_name))

                # Win / Loss / Draw summary cards
                if not win_loss_draw.empty:
                    row = win_loss_draw.iloc[0]
                    inner = ""
                    for col in win_loss_draw.columns:
                        is_red = col.lower().startswith("win")
                        cls = "value red" if is_red else "value"
                        inner += f"""
                        <div class="metric-card">
                            <div class="label">{col}</div>
                            <div class="{cls}">{row[col]}</div>
                        </div>"""
                    st.markdown(f'<div class="metric-grid">{inner}</div>', unsafe_allow_html=True)

                # Two-column opening layout
                col1, col2 = st.columns(2)
                with col1:
                    section_divider("Openings · All")
                    st.dataframe(openings, use_container_width=True)
                    section_divider("Win Rate by Opening")
                    st.dataframe(win_by_opening, use_container_width=True)
                with col2:
                    section_divider("Openings · White")
                    st.dataframe(white_openings, use_container_width=True)
                    section_divider("Openings · Black")
                    st.dataframe(black_openings, use_container_width=True)

                section_divider("Win Rate by Colour")
                st.dataframe(winrate_colour, use_container_width=True)

                section_divider("All Games")
                players_games = pd.DataFrame(
                    conn_manager.handle_SQL(select_player_all_games, player_name=player_name)
                )
                st.dataframe(players_games, use_container_width=True)


if __name__ == "__main__":
    main()