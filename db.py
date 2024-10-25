from config import Config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
engine = create_engine(Config.urlDB)
Session = sessionmaker(bind=engine)

# Dependencia para obtener la sesión de base de datos
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()