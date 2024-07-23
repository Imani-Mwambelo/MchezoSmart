from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from .. import crud, models, schemas, database

router = APIRouter(
    prefix="/contributions",
    tags=["Contributions"]
                   )

@router.post("/", response_model=schemas.Contribution)
def create_contribution(contribution: schemas.ContributionCreate, db: Session = Depends(database.get_db)):
    return crud.create_contribution(db=db, contribution=contribution)

@router.get("/tontine/{tontine_id}", response_model=List[schemas.Contribution])
def read_contributions_by_tontine(tontine_id: int, db: Session = Depends(database.get_db)):
    contributions = crud.get_contributions_by_tontine(db, tontine_id=tontine_id)
    return contributions

@router.get("/user/{user_id}", response_model=List[schemas.Contribution])
def read_contributions_by_user(user_id: int, db: Session = Depends(database.get_db)):
    contributions = crud.get_contributions_by_user(db, user_id=user_id)
    return contributions

@router.put("/{contribution_id}", response_model=schemas.Contribution)
def update_contribution(contribution_id: int, submitted: bool, db: Session = Depends(database.get_db)):
    db_contribution = crud.update_contribution(db, contribution_id=contribution_id, submitted=submitted)
    if not db_contribution:
        raise HTTPException(status_code=404, detail="Contribution not found")
    return db_contribution
