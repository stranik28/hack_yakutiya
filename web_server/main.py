from fastapi import FastAPI, HTTPException
import httpx
import json
import requests

app = FastAPI()

def send_post_request(message):
    url = "http://rasa_core:5005/webhooks/rest/webhook"
    rasa_response = requests.post(
        url,
        json={
            "sender": 1234,
            "message": message
        }
    ).json()
    answer = '\n'.join([item['text'] for item in rasa_response])
    if 'Извините, я не понял вашего вопроса' not in answer:
        return {
            'STATUS' : answer.split('%'),
            'CODE' : 200
        }
    return {'CODE' : 100}

@app.get("/process_message/")
def process_message(message: str):
    try:
        result = send_post_request(message)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/process_message/")
def process_message(message: str):
    try:
        result = send_post_request(message)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)