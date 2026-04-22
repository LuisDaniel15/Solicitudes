from pydantic import BaseModel

class SolicitudCreate(BaseModel):
    estudiante_id: int
    tipo: str
    descripcion: str

class SolicitudResponse(BaseModel):
    id: int
    codigo: str
    tipo: str
    estado_actual: str

    class Config:
        from_attributes = True

class CambiarEstado(BaseModel):
    estado: str
    comentario: str
    usuario_id: int