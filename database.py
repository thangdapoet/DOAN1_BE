from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# cau hinh ket noi sql
SQLALCHEMY_DATABASE_URL = "mssql+pyodbc://sa:12346@localhost\\SQLEXPRESS/DOAN1?driver=ODBC+Driver+17+for+SQL+Server"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()