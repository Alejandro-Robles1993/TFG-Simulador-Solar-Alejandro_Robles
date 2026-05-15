from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# ==================== CONFIGURACIÓN DE BASE DE DATOS ====================


p1 = "AVNS_etYagcTCktK"
p2 = "Myb4HVaZ"

URL_DATABASE = f"mysql+pymysql://doadmin:{p1}{p2}@db-mysql-ams3-48533-do-user-37311075-0.i.db.ondigitalocean.com:25060/defaultdb?ssl-mode=REQUIRED"

engine = create_engine(
    URL_DATABASE,
    pool_pre_ping=True,
    pool_recycle=3600
)

SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()