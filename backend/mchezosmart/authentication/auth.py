from fastapi import FastAPI, Response, status, HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import models, schemas
from . import oauth2, utils
from ..database import get_db

router=APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schemas.Token)
def login(user_credentials:OAuth2PasswordRequestForm= Depends(), db: Session=Depends(get_db)):
      

      usr=db.query(models.User).filter(models.User.email==user_credentials.username).first()
  
      
      if not usr:     
          raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail=f"Invalid cridentials, wrong email or password")
    
      if not utils.verify(user_credentials.password,usr.password):
          raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid cridentials, wrong email or password")
    
      access_token=oauth2.create_access_token(data={"id":usr.id, "role":usr.role})
      

      return {"access_token":access_token, "token_type":"bearer", "role":usr.role}



