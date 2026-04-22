def generar_codigo(db):
    from app.models.solicitud import Solicitud

    total = db.query(Solicitud).count() + 1
    return f"SOL-{str(total).zfill(4)}"