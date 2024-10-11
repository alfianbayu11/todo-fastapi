from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_checklists(db: Session, user_id: int):
    return db.query(models.Checklist).filter(models.Checklist.owner_id == user_id).all()

def create_checklist(db: Session, checklist: schemas.ChecklistCreate, user_id: int):
    db_checklist = models.Checklist(**checklist.dict(), owner_id=user_id)
    db.add(db_checklist)
    db.commit()
    db.refresh(db_checklist)
    return db_checklist

def get_items(db: Session, checklist_id: int):
    return db.query(models.ChecklistItem).filter(models.ChecklistItem.checklist_id == checklist_id).all()

def get_item(db: Session, item_id: int, checklist_id: int):
    return db.query(models.ChecklistItem).filter(models.ChecklistItem.id == item_id, models.ChecklistItem.checklist_id == checklist_id).first()

def create_item(db: Session, item: schemas.ItemCreate, checklist_id: int):
    db_item = models.ChecklistItem(**item.dict(), checklist_id=checklist_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, item: schemas.ItemCreate, db_item: models.ChecklistItem):
    db_item.item_name = item.item_name
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item_status(db: Session, item: models.ChecklistItem, status: bool):
    item.is_done = status
    db.commit()
    db.refresh(item)

def delete_item(db: Session, item: models.ChecklistItem):
    db.delete(item)
    db.commit()

def delete_checklist(db: Session, checklist: models.Checklist):
    db.delete(checklist)
    db.commit()
