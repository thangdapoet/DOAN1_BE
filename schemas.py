from pydantic import BaseModel
from datetime import datetime

class DataCreate(BaseModel):
    doam: float
    nhietdo: float
    ppm_co2: float
    ppm_co: float
    ppm_nh3: float
    ppm_toluen: float
    ppm_c6h6: float
    session_id: int
    
    class Config:
        orm_mode = True

class Data(DataCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class EmptyPayload(BaseModel):
    temp: int

    class Config:
        orm_mode = True

class Session(BaseModel):
    session_id: int
    created_at: datetime

    class Config:
        orm_mode = True