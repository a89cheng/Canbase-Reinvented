class Game:
    """
    The Game class answers the question: “What minimally defines a chess game?”
    The information to answer the question is found in the Game class
    """

    def __init__(self, date = None , event = None , site = None , round_num = None ,
                 white = None ,  black = None , result = None , eco=None , moves = None):
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

        if eco in empty_values:
            self.eco = None
        else:
            self.eco = eco

        if moves in empty_values:
            self.moves = None
        else:
            self.moves = moves


    def is_valid(self):
        """The is_valid method confirms whether a Game class object is actually a valid game"""

        #Could also have been done in one line with return bool(self.white and self.black and self.result in results)
        valid_results = ["1-0" , "0-1" , "1/2-1/2"]

        if self.white is None:
            return False
        if self.black is None:
            return False
        if self.result not in valid_results:
            return False

        return True

    def __str__(self):
        """The __str__ method serves for testing the outputs of a Game class object"""

        # Representation of an inline if-else
        white = str(self.white) if self.white is not None else "Unknown"
        black = str(self.black) if self.black is not None else "Unknown"
        date = str(self.date) if self.date is not None else "????-??-??"
        result = str(self.result) if self.result is not None else "Unknown"

        # Format: Alice vs Bob | 2025-12-13 | 1-0
        return f"{white} vs {black} | {date} | {result}"

    def __eq__(self, other):
        """Defines what equality between 2 Game objects mean, this depends on the players, date and result"""

        #Check that the input at hand is actually a Game object
        if not isinstance(other, Game):
            return NotImplemented

        return (
                self.white == other.white and
                self.black == other.black and
                self.date == other.date and
                self.result == other.result
        )
