from sqlalchemy.orm import Session
from models import Data, Session
import schemas

def get_product(session_id: int,db: Session):
    db_data = db.query(Data).where(Data.session_id == session_id)
    
    # Convert SQLAlchemy objects to dictionaries
    return [{"id": data.id,
              "doam": data.doam,
                "nhietdo": data.nhietdo,
                  "ppm_co2": data.co2,
                  "ppm_co": data.co,
                  "ppm_nh3": data.nh3,
                  "ppm_toluen": data.toluen,
                  "ppm_c6h6": data.c6h6,
                  "session_id": data.session_id,
                  "created_at": data.created_at} for data in db_data]

def get_latest_temperature(db: Session):
    latest = db.query(Data).order_by(Data.created_at.desc()).first()
    return {"id": latest.id,
              "doam": latest.doam,
                "nhietdo": latest.nhietdo,
                  "ppm_co2": latest.co2,
                  "ppm_co": latest.co,
                  "ppm_nh3": latest.nh3,
                  "ppm_toluen": latest.toluen,
                  "ppm_c6h6": latest.c6h6,
                  "session_id": latest.session_id,
                  "created_at": latest.created_at}

def get_all_session(db: Session):
    db_data = db.query(Session).all()

    return[{
        "session_id": data.id,
        "created_at": data.created_at,
    } for data in db_data]

def get_latest_session(db: Session):
    latest = db.query(Session).order_by(Session.created_at.desc()).first()
    return latest.id