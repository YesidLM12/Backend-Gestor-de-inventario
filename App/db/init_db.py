from app.db.session import engine,Base,SessionLocal
from app.models.user_model import User
from app.utils.enums import UserRole

def init_db():
    print("Creating database")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    existing_admin = db.query(User).filter(User.email == "admin@admin.com").first()

    if not existing_admin:
        admin = User(
            username="admin",
            email="admin@admin.com",
            role=UserRole.ADMIN,
            is_active=True,
            is_admin=True,
            hashed_password="admin",
        )
        db.add(admin)
        db.commit()
        print("Admin created successfully")
    else:
        print("Admin already exists")

    db.close()