from app.models.notificacion import Notificacion

def crear_notificacion(db, usuario_id, solicitud_id, mensaje):
    noti = Notificacion(
        usuario_id=usuario_id,
        solicitud_id=solicitud_id,
        mensaje=mensaje,
        tipo="telegram",
        enviado=False
    )
    db.add(noti)