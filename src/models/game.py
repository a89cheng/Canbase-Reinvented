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

        self.date = date
        self.event = event
        self.site = site

        #round is built into python and cannot be used as a variable name
        self.round_num = round_num

        self.white = white
        self.black = black
        self.result = result