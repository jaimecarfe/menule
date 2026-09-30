from app.database import SessionLocal
from app.services.auth_service import AuthService

db = SessionLocal()

try:

    user = AuthService.login(
        db,
        "admin@menule.com",
        "admin1234",
    )

    if user:
        print("SUCCESS")
        print(user.nombre)
        print(user.tipo)
    else:
        print("LOGIN FAILED")

finally:
    db.close()