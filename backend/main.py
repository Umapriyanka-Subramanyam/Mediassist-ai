import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
from .utils import get_medicine_info_from_llm

# Load environment variables
load_dotenv()

app = FastAPI(title="AI Medicine Information Assistant")

class MedicineRequest(BaseModel):
    medicine_name: str
    language: Optional[str] = "English"

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Medicine Assistant API is running"}

@app.post("/api/medicine-info")
def get_medicine_info(request: MedicineRequest):
    try:
        data = get_medicine_info_from_llm(request.medicine_name, request.language)
        return data
    except ValueError as e:
        # Pass the missing key error to frontend to display nicely
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
