import matplotlib.pyplot as plt
from matplotlib import style

def Eco_to_opening(Eco_code):
    """ECO (encyclopedia of chess openings) conversion to Opening name"""

    #Dictionary of generic Eco opening codes to their respective openings
    mapping_dict = {
        "A00": "Polish Opening",
        "A01": "Nimzovich-Larsen Attack",
        "A02-A03": "Bird's Opening",
        "A04-A09": "Reti Opening",
        "A10-A39": "English Opening",
        "A40": "Queen's Pawn Opening",
        "A41-A42": "Modern Defence",
        "A43-A44": "Old Benoni Defence",
        "A45": "Trompowsky Attack",
        "A46-A49": "Indian Defence",
        "A50": "Budapest Gambit Declined",
        "A51-A52": "Budapest Gambit",
        "A53-A55": "Old Indian Defence",
        "A56-A59": "Benko Gambit",
        "A60-A79": "Modern Benoni",
        "A80-A99": "Dutch Defence",
        "B00": "King's Pawn Opening",
        "B01": "Scandinavian Defence",
        "B02-B05": "Alekhine's Defence",
        "B06": "Modern Defence",
        "B07-B09": "Pirc Defence",
        "B10-B19": "Caro-Kann Defence",
        "B20-B99": "Sicilian Defence",
        "C00-C19": "French Defence",
        "C20": "King's Pawn Game",
        "C21-C22": "Centre Game",
        "C23-C24": "Bishop's Opening",
        "C25-C29": "Vienna Game",
        "C30-C39": "King's Gambit",
        "C40": "King's Knight Opening",
        "C41": "Philidor Defence",
        "C42-C43": "Petrov's Defence",
        "C44": "Scotch Gambit",
        "C45": "Scotch Game",
        "C46": "Three Knights Game",
        "C47-C49": "Four Knights Game",
        "C50-C59": "Italian Game",
        "C60-C99": "Ruy Lopez",
        "D00-D05": "Queen's Pawn Game",
        "D06-D09": "Queen's Gambit Declined Slav",
        "D10-D19": "Slav Defence",
        "D20-D29": "Queen's Gambit Accepted",
        "D30-D69": "Queen's Gambit Declined",
        "D70-D99": "Gruenfeld Defence",
        "E00-E09": "Catalan Opening",
        "E10-E19": "Queen's Indian Defence",
        "E20-E59": "Nimzo-Indian Defence",
        "E60-E99": "King's Indian Defence",
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

def plot_win_percentanges(results_df):
    style.use("dark_background")

    results_list = results_df.columns.tolist()
    plt.pie(results_df, colors=["green","grey","red"])

    plt.show()