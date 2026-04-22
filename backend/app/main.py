from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base
from app.api.routes import solicitudes

# Importar modelos para que SQLAlchemy los registre
from app.models import usuario, solicitud, documento, historial, notificacion

app = FastAPI()

# Crear tablas automáticamente
Base.metadata.create_all(bind=engine)


app.include_router(solicitudes.router, prefix="/solicitudes", tags=["Solicitudes"])
@app.get("/")
def root():
    return {"message": "API funcionando correctamente"}