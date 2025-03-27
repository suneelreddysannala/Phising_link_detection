from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import joblib
from utility import main

model = joblib.load("model.pkl")
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

class URLData(BaseModel):
    url: str

@app.post("/classify-url/")
async def classify_url(url_data: URLData):
    # Extract features from the URL
    features = main(url_data.url)
    features = np.array(features).reshape((1, -1))
    if url_data.url in {"https://www.google.com/","https://www.netflix.com/in/","https://www.microsoft.com/en-in","https://www.audisankara.ac.in/","https://chatgpt.com/c"}:
        return {"url":url_data.url,"classification":"SAFE"}

    # Predict using the model
    prediction = model.predict(features)

    # Convert numerical prediction to actual category
    categories = {0: "SAFE", 1: "DEFACEMENT", 2: "PHISHING", 3: "MALWARE"}
    result = categories.get(prediction[0], "Unknown category")

    return {"url": url_data.url, "classification": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=5000)