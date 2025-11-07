from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from datetime import datetime
from dotenv import load_dotenv
import os


app = FastAPI(title="Catnip Dispenser API")


load_dotenv()
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY not found in environment variables")


# temporary in memory counter and history
button_press_count = 0
press_history = []


class DispenseRequest(BaseModel):
    device_id: str


@app.get("/")
def home():
    return {
        "button_press_count": button_press_count
    }

@app.post("/api/v1/dispense/request")
def dispense(request: DispenseRequest, x_api_key: str = Header(...)):
    global button_press_count

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key.")

    button_press_count += 1
    
    press_history.append({
        "device_id":request.device_id,
        "timestamp": datetime.now().isoformat(),
        "button_press_count": button_press_count
    })

    print(f"Received request from device: {request.device_id}")
    
    return {
        "allowed": True,
        "device_id": request.device_id,
    }

@app.get("/api/v1/stats")
def get_stats():
    return {
        "button_press_count": button_press_count,
        "recent_presses": press_history[-10:]
    }
