from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.solicitud import Solicitud
from app.models.historial import HistorialEstado
from app.schemas.solicitud import SolicitudCreate
from app.utils.generador_codigo import generar_codigo
from app.schemas.solicitud import SolicitudCreate, CambiarEstado
from fastapi import HTTPException
from app.services.notificaciones import crear_notificacion

router = APIRouter()

# ✅ CREAR SOLICITUD
@router.post("/")
def crear_solicitud(data: SolicitudCreate, db: Session = Depends(get_db)):
    
    codigo = generar_codigo(db)

    nueva = Solicitud(
        codigo=codigo,
        estudiante_id=data.estudiante_id,
        tipo=data.tipo,
        descripcion=data.descripcion,
        estado_actual="radicada"
    )

    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    # 🔥 Crear historial automáticamente
    historial = HistorialEstado(
        solicitud_id=nueva.id,
        estado="radicada",
        comentario="Solicitud creada",
        usuario_id=data.estudiante_id
    )

    db.add(historial)
    db.commit()

    return nueva


# ✅ LISTAR SOLICITUDES
@router.get("/")
def listar_solicitudes(db: Session = Depends(get_db)):
    return db.query(Solicitud).all()


ESTADOS_VALIDOS = ["radicada", "en_revision", "aprobada", "rechazada"]
@router.put("/{solicitud_id}/estado")
def cambiar_estado(solicitud_id: int, data: CambiarEstado, db: Session = Depends(get_db)):

    solicitud = db.query(Solicitud).filter(Solicitud.id == solicitud_id).first()

    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")

    if data.estado not in ESTADOS_VALIDOS:
        raise HTTPException(status_code=400, detail="Estado inválido")

    solicitud.estado_actual = data.estado

    historial = HistorialEstado(
        solicitud_id=solicitud.id,
        estado=data.estado,
        comentario=data.comentario,
        usuario_id=data.usuario_id
    )

    db.add(historial)

    # 🔥 CREAR NOTIFICACIÓN
    mensaje = f"Tu solicitud {solicitud.codigo} ahora está en estado: {data.estado}"

    crear_notificacion(
        db=db,
        usuario_id=solicitud.estudiante_id,
        solicitud_id=solicitud.id,
        mensaje=mensaje
    )

    db.commit()

    return {"mensaje": "Estado actualizado y notificación creada"}


@router.get("/usuario/{usuario_id}")
def obtener_solicitudes_usuario(usuario_id: int, db: Session = Depends(get_db)):
    
    solicitudes = db.query(Solicitud).filter(Solicitud.estudiante_id == usuario_id).all()

    if not solicitudes:
        raise HTTPException(status_code=404, detail="No tiene solicitudes")

    return solicitudes


@router.get("/{solicitud_id}/estado")
def obtener_estado(solicitud_id: int, db: Session = Depends(get_db)):

    solicitud = db.query(Solicitud).filter(Solicitud.id == solicitud_id).first()

    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")

    return {
        "codigo": solicitud.codigo,
        "estado": solicitud.estado_actual
    }

from app.rag.rag_service import buscar_respuesta

@router.post("/chat")
def chat_rag(data: dict):
    pregunta = data["mensaje"]

    respuesta = buscar_respuesta(pregunta)

    return {
        "respuesta": respuesta
    }