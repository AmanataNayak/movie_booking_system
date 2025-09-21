from sqlalchemy.orm import Session
from database import engine
from models.user import User, UserRole
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_admin(db: Session):
    admin_username = "admin"
    admin_password = "admin123"
    email = "admin@gmail.com"

    existing = db.query(User).filter(User.username == admin_username).first()
    if existing:
        print("Admin already exists")
        return

    hashed_password = pwd_context.hash(admin_password)
    admin_user = User(username=admin_username, hashed_password=hashed_password, email=email, role=UserRole.admin)
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    print(f"Admin created: {admin_user.username}")


if __name__ == "__main__":
    db = Session(bind=engine)
    create_admin(db)