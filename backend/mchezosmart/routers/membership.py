from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, models, schemas, database
from ..authentication import oauth2

router = APIRouter()

@router.post("/memberships/", response_model=schemas.Membership)
def create_membership(membership: schemas.MembershipCreate, db: Session = Depends(database.get_db), current_user= Depends(oauth2.get_current_user)):
    return crud.create_membership(db=db, membership=membership)

@router.get("/memberships/{membership_id}", response_model=schemas.Membership)
def read_membership(membership_id: int, db: Session = Depends(database.get_db)):
    db_membership = crud.get_membership(db, membership_id=membership_id)
    if not db_membership:
        raise HTTPException(status_code=404, detail="Membership not found")
    return db_membership

@router.get("/memberships/tontine/{tontine_id}", response_model=List[schemas.Membership])
def read_memberships_by_tontine(tontine_id: int, db: Session = Depends(database.get_db)):
    memberships = crud.get_memberships_by_tontine(db, tontine_id=tontine_id)
    return memberships

@router.get("/memberships/user/{user_id}", response_model=List[schemas.Membership])
def read_memberships_by_user(user_id: int, db: Session = Depends(database.get_db)):
    memberships = crud.get_memberships_by_user(db, user_id=user_id)
    return memberships

@router.delete("/memberships/{membership_id}", response_model=schemas.Membership)
def delete_membership(membership_id: int, db: Session = Depends(database.get_db)):
    db_membership = crud.delete_membership(db, membership_id=membership_id)
    if not db_membership:
        raise HTTPException(status_code=404, detail="Membership not found")
    return db_membership
