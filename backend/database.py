# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# # Estructura: postgresql://USUARIO:PASSWORD@localhost:5432/NOMBRE_DB
# # Cambiá 'postgres' y 'tu_password' por tus credenciales reales
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin123@localhost:5432/cardiopredict_db"

# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# --- CAMBIO AQUÍ ---
# SQLite usa tres barras para una ruta relativa: sqlite:///nombre_archivo.db
SQLALCHEMY_DATABASE_URL = "sqlite:///cardiopredict_db.db"

# El argumento 'check_same_thread' es necesario solo para SQLite en Flask/FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# --------------------

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()