from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.db.base import Base

class Solicitud(Base):
    __tablename__ = "solicitudes"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, index=True)
    estudiante_id = Column(Integer, ForeignKey("usuarios.id"))
    tipo = Column(String)
    descripcion = Column(String)
    estado_actual = Column(String, default="radicada")
    prioridad = Column(String, default="media")
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow)