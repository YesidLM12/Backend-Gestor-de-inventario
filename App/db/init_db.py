from app.db.session import engine,Base,SessionLocal
from app.models.user import User
from app.models.supplier import Supplier

def init_db():
    print("Creating database")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    admin = db.query(User).filter(User.email == "admin@admin.com").first()
    if not admin:
        admin = User(
            username="admin",
            email="admin@admin.com",
            password="admin",
            role=UserRole.ADMIN,
            is_active=True,
            is_admin=True,
        )
        db.add(admin)
        db.commit()
    db.close()