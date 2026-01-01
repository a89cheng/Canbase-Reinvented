#Key concepts (streamlit syntax):
#st.title("My App") → shows a big title in the browser
#st.write("Hello!") → prints text
#st.file_uploader("Upload PGN") → lets users upload files
#st.dataframe(my_data) → shows tables
#st.bar_chart(my_data) → makes simple charts
#st.title("Chess Opening Explorer Test")

def main():
    import streamlit as st
    import chess.pgn
    import chess
    import pandas as pd
    import matplotlib
    import io

    st.title("Chess Opening Explorer Test")

    pgnfile = st.file_uploader("Upload PGN")

    game_info = [] #will take the games and just store header later

    if pgnfile is not None:
        #game = chess.pgn.read_game(pgnfile)
        st.write("File is uploaded!")
        text = pgnfile.read().decode("utf-8") #has to interpret to a string 
        pgnfile = io.StringIO(text) 
        pgnfile.seek(0) # ✅ Reset file pointer before reading (ChatGPT line)

     #pgn = open("pgnfile.pgn")  # your uploaded PGN file | is completely unecessary to open file... doesn't exist on disk?

        """
        The games list below isolates all the games in the PGN into individual ones
        The game_info goes through all the games in the list "games" and takes the header information
        This is a 2 step process of isolating the games and then extracting the data
        """

        games = []  # store game info dictionaries

        while True:
            game = chess.pgn.read_game(pgnfile) #Would assume that the function read_game reads only 1 game at a time hence, the games are stored accordingly
            if game is None:  # means end of file, this si done by default by python-chess
                break
            games.append(game) #Games are added to the game list and the headers will be stored in dictionaries

        for game in games: #For all games in a single pgn file...
            headers = game.headers
            game_info.append({
                "White": headers.get("White", "Unknown"),
                "Black": headers.get("Black", "Unknown"),
                "Result": headers.get("Result", "Unknown"),
                "Opening": headers.get("Opening", "Unknown"),
            }) #The headers are extracted and set equivalent to whatever they are in the game...

    if not game_info:
        st.warning("Please upload a PGN file first!")
        st.stop()

    df = pd.DataFrame(game_info) #the datafram is created and stored under df
    st.dataframe(df) # if you're in Streamlit
    username = st.text_input("Enter your Lichess username:")

    white_games = []
    black_games = []
    # Assume username is already collected via Streamlit
    # username = st.text_input("Enter your Lichess username:")

    # Split games by whether the user played as White or Black, parsing through the list of games' information
    for game in game_info:
        if game["White"] == username:
            white_games.append(game)
        elif game["Black"] == username:
            black_games.append(game)

    # Convert filtered lists to DataFrames
    df_white = pd.DataFrame(white_games)
    df_black = pd.DataFrame(black_games)

    # Check if there are even any games with the person's usernament (account could be new)
    if df_white.empty and df_black.empty:
        st.warning("No games found for that username.")
        st.stop()

    # Calculate top openings for each
    top_openings_white = df_white["Opening"].value_counts().head(5)
    top_openings_black = df_black["Opening"].value_counts().head(5)

    # Display results in Streamlit
    st.write("### Top 5 Openings | White")
    st.dataframe(top_openings_white)
    st.bar_chart(top_openings_white)

    st.write("### Top 5 Openings | Black")
    st.dataframe(top_openings_black)
    st.bar_chart(top_openings_black)

    white_result_counts = df_white["Result"].value_counts()
    black_result_counts = df_black["Result"].value_counts()
    result_counts = white_result_counts + black_result_counts

    st.write("### White Game Results")
    st.dataframe(white_result_counts)
    #st.pie_chart(white_result_counts)

    st.write("### Black Game Results")
    st.dataframe(black_result_counts)
    #st.pie_chart(black_result_counts)

    st.write("### Total Game Results")
    st.dataframe(result_counts)
    #st.pie_chart(result_counts)

    #pie charts don't actually exist... need matplotlib in order to make them

if __name__ == "__main__": 
    main()



#data = pgnfile.read()  # bytes

#lines = text.splitlines()
#st.write(lines[:10])  # show first 10 lines

#text = data.decode("utf-8")  # string and "utf-8" tells the computer how to convert those 0s and 1s back into human-readable characters
#st.write(text[:100])  # first 100 characters


#PGN Subheadings typically include:
#Typical headers are:
#Event, Site, Date
#White, Black
#Result
#Opening, ECO