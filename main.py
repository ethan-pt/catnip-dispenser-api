from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel


app = FastAPI(title="Catnip Dispenser API")

API_KEY = "temp_key" # this will be moved to a .env file, just testing stuff for now

class DispenseRequest(BaseModel):
    device_id: str

@app.post("/api/v1/dispense/request")
def dispense(request: DispenseRequest, x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key.")

    print(f"Received request from device: {request.device_id}")
    
    return {
        "allowed": True,
        "device_id": request.device_id
    }
