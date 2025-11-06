from fastapi import FastAPI


app = FastAPI(title="Catnip Dispenser API")

@app.get("/")
def read_root():
    return {"message": "bug stinks"}

@app.post("/api/v1/dispense/request")
def dispense():
    return {"allowed": True}
