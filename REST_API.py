from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import pickle
import re

# Create a FastAPI instance
app=FastAPI()

# Serve static files (HTML and CSS)
app.mount('/static', StaticFiles(directory='static'), name='static')

# Load the language detection model from the model directory
model=pickle.load(open('model/language_detection_model.pkl','rb')) 

# Define a Pydantic model for the text input
class Text(BaseModel):
    text:str

# Define a GET endpoint at the root route ("/") that returns the UI HTML file
@app.get('/', response_class=HTMLResponse)
async def root():
    with open('static/ui.html', 'r') as file:
        return file.read()

# Define a POST endpoint at the /predict route that takes an instance of Text
# and returns the predicted language
@app.post('/predict', response_class=JSONResponse)
async def predict_sentence_language(text_input:Text):
    
    # Extract the text from the Text instance and remove special characters
    text = [re.sub(r'[!@#$(),\n"%^\*\?\:;~`0-9\.\[\]\+\-\'=£]', '', text_input.text.lower())]

    # Make a prediction using the loaded model
    prediction = model.predict(text)

    # Return the predicted language (1 for Italian and 0 for Non-Italian)
    return {"prediction": prediction.tolist()[0]}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)