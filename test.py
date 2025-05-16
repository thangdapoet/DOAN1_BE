from sqlalchemy import create_engine


connection_string = "mssql+pyodbc://sa:12346@localhost\SQLEXPRESS:1433/DOAN1?driver=ODBC+Driver+17+for+SQL+Server"


engine = create_engine(connection_string)


try:
    with engine.connect() as conn:
        print("Connection successful!")
except Exception as e:
    print("Connection failed:", e)