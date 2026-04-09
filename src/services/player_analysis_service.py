from src.db.connection_manager import Connection_Manager
from src.analytics.queries import *
import pandas as pd

#A relatively dubious function LOL... just a means of grouping AI related dfs
def player_df_creation(conn_manager, player_name):

    white_openings = pd.DataFrame(conn_manager.handle_SQL(player_openings_white, player_name=player_name))
    black_openings = pd.DataFrame(conn_manager.handle_SQL(player_openings_black, player_name=player_name))
    win_by_opening = pd.DataFrame(conn_manager.handle_SQL(win_rate_by_opening, player_name=player_name))

    winrate_colour = pd.DataFrame(conn_manager.handle_SQL(player_winrate_by_colour, player_name=player_name))
    win_loss_draw = pd.DataFrame(conn_manager.handle_SQL(player_win_loss_draw_and_decisive_game_percent, player_name=player_name))

    return white_openings , black_openings, win_by_opening , winrate_colour, win_loss_draw