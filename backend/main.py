from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import difflib
import logging

app = FastAPI()

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Message(BaseModel):
    content: str

class ChatResponse(BaseModel):
    response: str

# Function to load the Excel file
def load_excel_file():
    xlsx_path = 'school.xlsx'
    try:
        faq_df = pd.read_excel(xlsx_path, sheet_name='FAQ')
        conversation_df = pd.read_excel(xlsx_path, sheet_name='Conversation')

        if 'Question' not in faq_df.columns or 'Response' not in faq_df.columns:
            raise ValueError("FAQ sheet must contain 'Question' and 'Response' columns.")
        if 'Greeting' not in conversation_df.columns or 'Praising' not in conversation_df.columns or 'Ending' not in conversation_df.columns:
            raise ValueError("Conversation sheet must contain 'Greeting', 'Praising', and 'Ending' columns.")

        # Convert all relevant columns to strings and fill NaN with empty strings
        faq_df['Question'] = faq_df['Question'].astype(str).fillna('')
        faq_df['Response'] = faq_df['Response'].astype(str).fillna('')
        conversation_df['Greeting'] = conversation_df['Greeting'].astype(str).fillna('')
        conversation_df['Praising'] = conversation_df['Praising'].astype(str).fillna('')
        conversation_df['Ending'] = conversation_df['Ending'].astype(str).fillna('')
        conversation_df['Question'] = conversation_df['Question'].astype(str).fillna('')
        conversation_df['Answer'] = conversation_df['Answer'].astype(str).fillna('')

        logger.debug("Excel file loaded successfully.")
        return faq_df, conversation_df
    except Exception as e:
        logger.error(f"Error loading Excel file: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: Could not load Excel file. {e}")

# Load the Excel file on startup
faq_df, conversation_df = load_excel_file()

# Define functions to handle various types of inputs
def in_cquestion(user_input):
    questions = conversation_df['Question'].str.lower().tolist()
    answers = conversation_df['Answer'].tolist()
    for i in range(len(questions)):
        if questions[i] in user_input:
            return answers[i]
    return None

def in_faq(user_input):
    questions = faq_df['Question'].str.lower().tolist()
    responses = faq_df['Response'].tolist()
    logger.debug(f"User input: {user_input}")
    logger.debug(f"FAQ questions: {questions}")
    closest_match = difflib.get_close_matches(user_input, questions, n=1, cutoff=0.6)
    logger.debug(f"Closest match: {closest_match}")
    if closest_match:
        return responses[questions.index(closest_match[0])]
    return None

def in_greeting(user_input):
    greetings = conversation_df['Greeting'].str.lower().tolist()
    for phrase in greetings:
        if phrase in user_input:
            return f"{phrase.capitalize()}, how may I assist you?"
    return None

def in_praising(user_input):
    praising = conversation_df['Praising'].str.lower().tolist()
    for phrase in praising:
        if phrase in user_input:
            return "Thanks a lot, always happy to help"
    return None

def in_ending(user_input):
    ending = conversation_df['Ending'].str.lower().tolist()
    for phrase in ending:
        if phrase in user_input:
            return "Goodbye! Talk to you later. Hope I could help you out."
    return None

@app.post("/chat", response_model=ChatResponse)
async def chat(message: Message):
    try:
        user_input = message.content.lower().strip()
        
        # Check various types of responses
        response = (in_greeting(user_input) or
                    in_cquestion(user_input) or
                    in_faq(user_input) or
                    in_praising(user_input) or
                    in_ending(user_input) or
                    "Sorry, I couldn't understand that. Please contact the reception for more info.")
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

    logger.debug(f"Response: {response}")
    return ChatResponse(response=response)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
