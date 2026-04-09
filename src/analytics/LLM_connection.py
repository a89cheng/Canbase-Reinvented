import os
from dotenv import load_dotenv
from google import generativeai as genai
import json

# Source of the API key: aistudio.google.com
# Research: google-generativeai python quickstart
# json_dict → prompt string → HTTP request to Gemini → text reply

def generate_report(json_dict):

    load_dotenv()
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    #Is the login of the process
    genai.configure(api_key=GEMINI_API_KEY)

    #Creating the model & saving it
    model = genai.GenerativeModel("gemini-3-flash-preview")

    #Interesting that the model is only specified by the user
    try:
        response = model.generate_content(
            contents=f"Pretend to be an expert chess coach"
                     f"Here is a player's statistical profile in JSON format:"
                     f"{json.dumps(json_dict)}"
                     f"Provide exactly these five sections: Player Summary, Opening Choice (and counters / strong openings against them), "
                     f"Strengths, Weaknesses, Playstyle Description (based on opening choices and noticeable trends)"
                     f"For each section use a header followed by 2-3 sentences at most"
        )
    except Exception as e:
        return None


    #Turn it back into a text string, otherwise it would be a response obj.
    output = response.text

    return output