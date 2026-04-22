from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.db.base import Base

class HistorialEstado(Base):
    __tablename__ = "historial_estados"

    id = Column(Integer, primary_key=True)
    solicitud_id = Column(Integer, ForeignKey("solicitudes.id"))
    estado = Column(String)
    comentario = Column(String)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    fecha = Column(DateTime, default=datetime.utcnow)