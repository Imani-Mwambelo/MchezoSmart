from fastapi import FastAPI
from .routers import user, tontine, membership, contribution
from .authentication import auth
from . import models, schemas
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(tontine.router)
app.include_router(auth.router)
app.include_router(membership.router)
app.include_router(contribution.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to Mchezo Smart"}
