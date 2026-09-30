from app.database import SessionLocal
from app.services.user_service import UserService

db = SessionLocal()

try:

    users = UserService.get_all_users(db)

    print(f"{len(users)} users")

    admin = UserService.get_user_by_email(
        db,
        "admin@menule.com",
    )

    print(admin.nombre)

finally:
    db.close()