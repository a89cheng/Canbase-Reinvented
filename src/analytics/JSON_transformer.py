import pandas as pd

def transform_dataframe(win_loss_draw_df = None, white_op_df = None,
                        black_op_df = None, opening_wr_df = None,
                        winrate_colour_df = None):

    data = {}
    data["overall"] = {}
    data["white_openings"]= {}
    data["black_openings"] = {}

    #Trying to find the overall stats
    if win_loss_draw_df and winrate_colour_df:
        wins = win_loss_draw_df.iloc[0]["wins"]
        data["overall"]["wins"] = wins

        losses = win_loss_draw_df.iloc[0]["losses"]
        data["overall"]["losses"] = losses

        draws = win_loss_draw_df.iloc[0]["draws"]
        data["overall"]["draws"] = draws

        decisive_percentage = win_loss_draw_df.iloc[0]["decisive_percentage"]
        data["overall"]["decisive_percentage"] = decisive_percentage

        white_win_percentage = winrate_colour_df.iloc[0]["White_Win_Percent"]
        data["overall"]["White_Win_Percent"] = white_win_percentage

        black_win_percentage = winrate_colour_df.iloc[0]["Black_Win_Percent"]
        data["overall"]["Black_Win_Percent"] = black_win_percentage

    #This part requires the index to be set so that the Eco is the main key in the dicts...
    """
    Because set_index() and to_dict() are two separate operations.
    set_index("Eco") reorganizes the DataFrame so ECO is the index instead of 0, 1, 2. 
    But it's still a DataFrame.to_dict() then converts that DataFrame to a dict. 
    The orient parameter tells it how to structure that dict. Without orient="index", 
    it will still give you a column-oriented dict even if the index is set correctly.
    orient="index" specifically means "use the index value as the outer key, and nest 
    the column values inside" — which is what you want. They work together. Fix both lines.
    """

    #index goes row by row, which groups name with the percentage

    if white_op_df and opening_wr_df:
        white_openings_df = pd.merge(white_op_df, opening_wr_df, on='Eco')
        white_opening_index = white_openings_df.set_index("Eco")
        white_openings = white_opening_index.to_dict(orient="index")
        data["white_openings"] = white_openings


    if black_op_df and opening_wr_df:
        black_openings_df = pd.merge(black_op_df, opening_wr_df, on='Eco')
        black_opening_index = black_openings_df.set_index("Eco")
        black_openings = black_opening_index.to_dict(orient="index")
        data["black_openings"] = black_openings

    #Complete dict of all the information being sent to the LLM,
    #Needs to be transformed into a JSON file first
    return data