from sqlalchemy.orm import Session
import app.models as models
import app.schemas as schemas
from passlib.hash import bcrypt

def create_user(db: Session, user: schemas.UserCreate):
    hashed = bcrypt.hash(user.password)
    db_user = models.User(username=user.username, email=user.email, password_hash=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_observation(db: Session, obs: schemas.ObservationCreate):
    db_obs = models.Observation(**obs.dict())
    db.add(db_obs)
    db.commit()
    db.refresh(db_obs)
    return db_obs
