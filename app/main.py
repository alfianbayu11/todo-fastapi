from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from . import crud, models, schemas, database, auth
from .dependencies import get_db, get_current_user
from app.database import Base, engine

# Buat tabel secara otomatis
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/register/", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)


@app.post("/login/")
def login(login_data: schemas.LoginRequest, db: Session = Depends(database.get_db)):
    user = crud.get_user_by_username(db, username=login_data.username)
    if not user or not crud.verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/checklists/", response_model=List[schemas.Checklist])
def read_checklists(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    checklists = crud.get_checklists(db, user_id=current_user.id)
    return checklists

@app.post("/checklists/", response_model=schemas.Checklist)
def create_checklist(checklist: schemas.ChecklistCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_checklist(db=db, checklist=checklist, user_id=current_user.id)

@app.delete("/checklists/{checklist_id}")
def delete_checklist(checklist_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    checklist = crud.get_checklist(db, checklist_id=checklist_id, user_id=current_user.id)
    if checklist is None:
        raise HTTPException(status_code=404, detail="Checklist not found")
    crud.delete_checklist(db=db, checklist=checklist)
    return {"msg": "Checklist deleted successfully"}

@app.get("/checklists/{checklist_id}/items", response_model=List[schemas.Item])
def get_items(checklist_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    items = crud.get_items(db, checklist_id=checklist_id)
    return items

@app.post("/checklists/{checklist_id}/items", response_model=schemas.Item)
def create_item(checklist_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_item(db=db, item=item, checklist_id=checklist_id)

@app.put("/checklists/{checklist_id}/items/{item_id}", response_model=schemas.Item)
def update_item(checklist_id: int, item_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_item = crud.get_item(db, item_id=item_id, checklist_id=checklist_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return crud.update_item(db=db, item=item, db_item=db_item)

@app.delete("/checklists/{checklist_id}/items/{item_id}")
def delete_item(checklist_id: int, item_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_item = crud.get_item(db, item_id=item_id, checklist_id=checklist_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    crud.delete_item(db=db, item=db_item)
    return {"msg": "Item deleted successfully"}

@app.put("/checklists/{checklist_id}/items/{item_id}/status")
def update_item_status(checklist_id: int, item_id: int, status: bool, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_item = crud.get_item(db, item_id=item_id, checklist_id=checklist_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    crud.update_item_status(db=db, item=db_item, status=status)
    return {"msg": "Status updated successfully"}
