from app.database import SessionLocal
from app.models import Usuario

db = SessionLocal()

try:
    users = db.query(Usuario).all()

    print(f"{len(users)} users found")

    for u in users[:5]:
        print(u.id_usuario, u.nombre, u.email, u.tipo)

finally:
    db.close()