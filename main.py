from fastapi import FastAPI, Depends, HTTPException, WebSocket
from sqlalchemy.orm import Session
import schemas
import crud
import database
import models 
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import logging

app = FastAPI()

# Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # <-- Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(database.get_db)):
    await websocket.accept()
    last_data = None
    last_session = None
    try:
        while True:
            current_data = crud.get_latest_temperature(db)
            current_session = crud.get_latest_session(db)

            if current_session != last_session:
                await websocket.send_text("getNewSession")
                last_session = current_session

            if current_data != last_data:
                await websocket.send_text("update")
                last_data = current_data

            await asyncio.sleep(5)
    except Exception as e:
        print("WebSocket disconnected:", e)


@app.get("/data/temperature/latest", response_model=schemas.Data)
def read_latest_temperature(db: Session = Depends(database.get_db)):
    return crud.get_latest_temperature(db)

@app.get("/")
def read_root():
    return {"DO AN 1 HUYNH QUANG THANG"} 

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.get("/data/{session_id}", response_model=list[schemas.Data])
def get_data(session_id: int,db: Session = Depends(database.get_db)):
    return crud.get_product(session_id ,db)

@app.post("/session/")
def receive_session(empty_payload: schemas.EmptyPayload ,db: Session = Depends(database.get_db)):
    try:
        new_session = models.Session()
        db.add(new_session)
        db.commit()
        db.refresh(new_session)
        return {
            "status": "success",
            "message": "Data received",
            "id": new_session.id
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/session/", response_model=list[schemas.Session])
def get_all_session(db: Session = Depends(database.get_db)):
    return crud.get_all_session(db)

@app.post("/api/sensor-data")
def receive_data(sensor_data: schemas.DataCreate, db: Session = Depends(database.get_db)):
    try:
        new_data = models.Data(
            nhietdo=sensor_data.nhietdo,
            doam=sensor_data.doam,
            co2=sensor_data.ppm_co2,
            co=sensor_data.ppm_co,
            nh3=sensor_data.ppm_nh3,
            toluen=sensor_data.ppm_toluen,
            c6h6=sensor_data.ppm_c6h6,
            session_id=sensor_data.session_id
        )
        db.add(new_data)
        db.commit()
        db.refresh(new_data)
        return {
            "status": "success",
            "message": "Data received",
            "data": {
                "id": new_data.id,
                "temperature": new_data.nhietdo,
                "humidity": new_data.doam,
                "co2": new_data.co2
            }
        }
    except Exception as e:
        db.rollback()
        logging.error(f"Sensor data error: {e}", exc_info=True)  # Logs traceback too
        raise HTTPException(status_code=500, detail=str(e))