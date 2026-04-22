from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey
from datetime import datetime
from app.db.base import Base

class Documento(Base):
    __tablename__ = "documentos"

    id = Column(Integer, primary_key=True)
    solicitud_id = Column(Integer, ForeignKey("solicitudes.id"))
    nombre_archivo = Column(String)
    ruta = Column(String)
    tipo_documento = Column(String)
    valido = Column(Boolean, default=False)
    confianza_yolo = Column(Float, default=0.0)
    fecha_subida = Column(DateTime, default=datetime.utcnow)