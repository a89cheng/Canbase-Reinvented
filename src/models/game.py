class Game:
    """
    The Game class answers the question: “What minimally defines a chess game?”
    The information to answer the question is found in the Game class
    """

    def __init__(self, date = None , event = None , site = None , round_num = None ,
                 white = None ,  black = None , result = None):
        """ Takes in the parsed information of PGN and turns all the headers into variables in the
         Game object to be stored; non-parsed data will be ignored for the time being.
         The core information (make the game what it is) is prioritized with elos and openings
         ignored for the time being"""

        empty_values = [ "?", "*", "????.??.??" ]

        if date in empty_values:
            self.date = None
        else:
            self.date = date

        if event in empty_values:
            self.event = None
        else:
            self.event = event

        if site in empty_values:
            self.site = None
        else:
            self.site = site

        #round is built into python and cannot be used as a variable name
        if round_num in empty_values:
            self.round_num = None
        else:
            self.round_num = round_num

        if white in empty_values:
            self.white = None
        else:
            self.white = white

        if black in empty_values:
            self.black = None
        else:
            self.black = black

        if result in empty_values:
            self.result = None
        else:
            self.result = result