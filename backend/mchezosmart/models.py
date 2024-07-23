from typing import Optional
from sqlalchemy import Column, ForeignKey, Integer, String, Date, text, BOOLEAN
from sqlalchemy.sql.sqltypes import TIMESTAMP
from datetime import timedelta
from sqlalchemy.orm import relationship, validates
from .database import Base
from uuid import uuid4

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False, default="user")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    tontines = relationship("Tontine", back_populates="creator")

class Tontine(Base):
    __tablename__ = 'tontines'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    start_date = Column(Date, nullable=False)
    days_per_cycle = Column(Integer, nullable=False)
    interval = Column(Integer, nullable=False)
    number_of_members = Column(Integer, nullable=False)
    end_date = Column(Date, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    #enrollment_key = Column(String, nullable=False, server_default=text('uuid4()'))

    creator = relationship("User", back_populates="tontines")
    memberships = relationship("Membership", back_populates="tontine")

    @property
    def end_date(self):
        return self.start_date + timedelta(days=self.number_of_members * self.days_per_cycle)

class Membership(Base):
    __tablename__ = 'memberships'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    tontine_id = Column(Integer, ForeignKey('tontines.id'), nullable=False)
    membership_count=Column(Integer, nullable=False, server_default=text('1'))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    user = relationship("User", back_populates="memberships")
    tontine = relationship("Tontine", back_populates="memberships")

User.memberships = relationship("Membership", back_populates="user")

class Contribution(Base):
    __tablename__ = 'contributions'
    id = Column(Integer, primary_key=True, index=True)
    tontine_id = Column(Integer, ForeignKey('tontines.id'), nullable=False)
    membership_id = Column(Integer, ForeignKey('memberships.id'), nullable=False)
    contribution_date = Column(Date, nullable=False)
    submitted = Column(BOOLEAN, nullable=False, server_default=text('False'))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
