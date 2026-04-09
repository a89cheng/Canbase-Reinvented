import pandas as pd
import json

def transform_dataframe(white_op_df = None , black_op_df = None ,
                        opening_wr_df = None, winrate_colour_df = None ,
                        win_loss_draw_df = None ):

    white_op_df["games_played"] = white_op_df["games_played"].astype(int)
    black_op_df["games_played"] = black_op_df["games_played"].astype(int)
    opening_wr_df["Win_Percent"] = opening_wr_df["Win_Percent"].astype(float)
    winrate_colour_df["White_Win_Percent"] = winrate_colour_df["White_Win_Percent"].astype(float)
    winrate_colour_df["Black_Win_Percent"] = winrate_colour_df["Black_Win_Percent"].astype(float)
    win_loss_draw_df["decisive_percentage"] = win_loss_draw_df["decisive_percentage"].astype(float)
    win_loss_draw_df["wins"] = win_loss_draw_df["wins"].astype(int)
    win_loss_draw_df["losses"] = win_loss_draw_df["losses"].astype(int)
    win_loss_draw_df["draws"] = win_loss_draw_df["draws"].astype(int)

    json_dict = {}
    json_dict["overall"] = {}
    json_dict["white_openings"]= {}
    json_dict["black_openings"] = {}

    #Trying to find the overall stats
    if win_loss_draw_df is not None and winrate_colour_df is not None:
        wins = win_loss_draw_df.iloc[0]["wins"]
        json_dict["overall"]["wins"] = wins

        losses = win_loss_draw_df.iloc[0]["losses"]
        json_dict["overall"]["losses"] = losses

        draws = win_loss_draw_df.iloc[0]["draws"]
        json_dict["overall"]["draws"] = draws

        decisive_percentage = win_loss_draw_df.iloc[0]["decisive_percentage"]
        print(decisive_percentage)
        json_dict["overall"]["decisive_percentage"] = decisive_percentage

        white_win_percentage = winrate_colour_df.iloc[0]["White_Win_Percent"]
        print(white_win_percentage)
        json_dict["overall"]["White_Win_Percent"] = white_win_percentage

        black_win_percentage = winrate_colour_df.iloc[0]["Black_Win_Percent"]
        print(black_win_percentage)
        json_dict["overall"]["Black_Win_Percent"] = black_win_percentage

    #index goes row by row, which groups name with the percentage

    if white_op_df is not None and opening_wr_df is not None:
        white_openings_df = pd.merge(white_op_df, opening_wr_df, on='Eco')
        white_opening_index = white_openings_df.set_index("Eco")
        white_openings = white_opening_index.to_dict(orient="index")
        print(white_openings)
        json_dict["white_openings"] = white_openings


    if black_op_df is not None and opening_wr_df is not None:
        black_openings_df = pd.merge(black_op_df, opening_wr_df, on='Eco')
        black_opening_index = black_openings_df.set_index("Eco")
        black_openings = black_opening_index.to_dict(orient="index")
        print(black_openings)
        json_dict["black_openings"] = black_openings

    #Complete dict of all the information being sent to the LLM,
    #Needs to be transformed into a JSON file first
    formatted_json_dict = json.loads(json.dumps(json_dict, default=str))

    return formatted_json_dict


"""
    Because set_index() and to_dict() are two separate operations.
    set_index("Eco") reorganizes the DataFrame so ECO is the index instead of 0, 1, 2. 
    But it's still a DataFrame.to_dict() then converts that DataFrame to a dict. 
    The orient parameter tells it how to structure that dict. Without orient="index", 
    it will still give you a column-oriented dict even if the index is set correctly.
    orient="index" specifically means "use the index value as the outer key, and nest 
    the column values inside" — which is what you want. They work together. Fix both lines.
"""