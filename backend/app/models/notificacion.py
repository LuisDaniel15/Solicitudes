from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime
from app.db.base import Base

class Notificacion(Base):
    __tablename__ = "notificaciones"

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    solicitud_id = Column(Integer, ForeignKey("solicitudes.id"))
    mensaje = Column(String)
    tipo = Column(String)
    enviado = Column(Boolean, default=False)
    fecha = Column(DateTime, default=datetime.utcnow)