from sqlalchemy.orm import Session
from . import models, schemas
from .authentication import utils
from datetime import timedelta

#user crud operations
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = utils.hash_password(user.password)
    db_user = models.User(name=user.name, email=user.email, password=hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        if user.name:
            db_user.name = user.name
        if user.email:
            db_user.email = user.email
        if user.role:
            db_user.role = user.role
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user



#tontine crud operations
def get_tontine(db: Session, tontine_id: int):
    return db.query(models.Tontine).filter(models.Tontine.id == tontine_id).first()

def get_tontines(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Tontine).offset(skip).limit(limit).all()

def create_tontine(db: Session, tontine: schemas.TontineCreate):
    db_tontine = models.Tontine(
        name=tontine.name,
        creator_id=tontine.creator_id,
        start_date=tontine.start_date,
        days_per_cycle=tontine.days_per_cycle,
        interval=tontine.interval,
        number_of_members=tontine.number_of_members
    )
    db.add(db_tontine)
    db.commit()
    db.refresh(db_tontine)
    return db_tontine

def update_tontine(db: Session, tontine_id: int, tontine: schemas.TontineUpdate):
    db_tontine = db.query(models.Tontine).filter(models.Tontine.id == tontine_id).first()
    if db_tontine:
        for key, value in tontine.model_dump().items():
            if value is not None:
                setattr(db_tontine, key, value)
        db.commit()
        db.refresh(db_tontine)
    return db_tontine

def delete_tontine(db: Session, tontine_id: int):
    db_tontine = db.query(models.Tontine).filter(models.Tontine.id == tontine_id).first()
    if db_tontine:
        db.delete(db_tontine)
        db.commit()
    return db_tontine

#membership crud operations
def create_membership(db: Session, membership=schemas.Membership):
    db_membership = models.Membership(
        user_id=membership.user_id,
        tontine_id=membership.tontine_id,
        membership_count=membership.membership_count
    )
    db.add(db_membership)
    db.commit()
    db.refresh(db_membership)
    return db_membership

def get_membership(db: Session, membership_id: int):
    return db.query(models.Membership).filter(models.Membership.id == membership_id).first()

def get_memberships_by_tontine(db: Session, tontine_id: int):
    return db.query(models.Membership).filter(models.Membership.tontine_id == tontine_id).all()

def get_memberships_by_user(db: Session, user_id: int):
    return db.query(models.Membership).filter(models.Membership.user_id == user_id).all()

def delete_membership(db: Session, membership_id: int):
    db_membership = db.query(models.Membership).filter(models.Membership.id == membership_id).first()
    if db_membership:
        db.delete(db_membership)
        db.commit()
    return db_membership


#contributions crud operations
def create_contribution(db: Session, contribution:schemas.ContributionCreate):
    db_contribution = models.Contribution(
        tontine_id=contribution.tontine_id,
        membership_id=contribution.membership_id,
        contribution_date=contribution.contribution_date,
        submitted=contribution.submitted
    )
    db.add(db_contribution)
    db.commit()
    db.refresh(db_contribution)
    return db_contribution

def get_contributions_by_tontine(db: Session, tontine_id: int):
    return db.query(models.Contribution).filter(models.Contribution.tontine_id == tontine_id).all()

def get_contributions_by_user(db: Session, user_id: int):
    return db.query(models.Contribution).join(models.Membership).filter(models.Membership.user_id == user_id).all()

def update_contribution(db: Session, contribution_id: int, submitted: bool):
    db_contribution = db.query(models.Contribution).filter(models.Contribution.id == contribution_id).first()
    if db_contribution:
        db_contribution.submitted = submitted
        db.commit()
        db.refresh(db_contribution)
    return db_contribution
