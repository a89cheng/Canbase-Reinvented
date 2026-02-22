def Eco_to_opening(Eco_code):
    """ECO (encyclopedia of chess openings) conversion to Opening name"""

    #Dictionary of generic Eco opening codes to their respective openings
    mapping_dict = {
        "A00": "Polish Opening",
        "A01": "Nimzovich-Larsen Attack",
        "A02-A03": "Bird's Opening",
        "A04-A09": "Reti Opening",
        "A10-A39": "English Opening",
        "B00": "King's Pawn Opening",
        "B01": "Scandinavian Defence",
        "B02-B05": "Alekhine's Defence",
        "B10-B19": "Caro-Kann Defence",
        "B20-B99": "Sicilian Defence",
        "C00-C19": "French Defence",
        "C50-C59": "Ruy Lopez",
        "D00-D69": "Queen's Gambit",
        "D70-D99": "Neo-Gruenfeld / Gruenfeld Defence",
        "E00-E59": "Nimzo-Indian / Catalan",
        "E60-E99": "King's Indian Defence"
    }

    #If the eco code is not a string, it is unknown
    if not isinstance(Eco_code, str):
        return "Unknown"

    #Iterates through each of the dictionary indices to find the right code;
    for code, name in mapping_dict.items():
        #There are sometimes ranges so we split them there
        if "-" in code:
            start, end = code.split("-")
            if start <= Eco_code <= end:
                opening_name = name
                return opening_name
        else:
            if Eco_code == code:
                opening_name = name
                return opening_name

    return "Unknown Opening"

def plot_opening_percentanges(dataframe):
    pass