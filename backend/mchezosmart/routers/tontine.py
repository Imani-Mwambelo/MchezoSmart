from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/tontines",
    tags=["tontines"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.Tontine)
def create_tontine(tontine: schemas.TontineCreate, db: Session = Depends(get_db)):
    return crud.create_tontine(db=db, tontine=tontine)

@router.get("/", response_model=List[schemas.Tontine])
def read_tontines(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    tontines = crud.get_tontines(db, skip=skip, limit=limit)
    return tontines

@router.get("/{tontine_id}", response_model=schemas.Tontine)
def read_tontine(tontine_id: int, db: Session = Depends(get_db)):
    db_tontine = crud.get_tontine(db, tontine_id=tontine_id)
    if db_tontine is None:
        raise HTTPException(status_code=404, detail="Tontine not found")
    return db_tontine

@router.put("/{tontine_id}", response_model=schemas.Tontine)
def update_tontine(tontine_id: int, tontine: schemas.TontineUpdate, db: Session = Depends(get_db)):
    db_tontine = crud.get_tontine(db, tontine_id=tontine_id)
    if db_tontine is None:
        raise HTTPException(status_code=404, detail="Tontine not found")
    return crud.update_tontine(db=db, tontine_id=tontine_id, tontine=tontine)

@router.delete("/{tontine_id}", response_model=schemas.Tontine)
def delete_tontine(tontine_id: int, db: Session = Depends(get_db)):
    db_tontine = crud.get_tontine(db, tontine_id=tontine_id)
    if db_tontine is None:
        raise HTTPException(status_code=404, detail="Tontine not found")
    return crud.delete_tontine(db=db, tontine_id=tontine_id)
