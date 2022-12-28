import sys
sys.path.append('..')
import models, schemas
from database import engine, SessionLocal
from routers.auth import get_current_user, get_user_exception, verify_password, get_password_hash
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session


router = APIRouter(
	prefix='/users',
	tags=['users'],
	responses={404: {'description': 'Not Found'}}
)
models.Base.metadata.create_all(bind=engine)


def get_db():
	try:
		db = SessionLocal()
		yield db
	finally:
		db.close()


@router.get('/')
async def read_all(db: Session = Depends(get_db)):
	return db.query(models.Users).all()

@router.get('/user/{user_id}')
async def user_by_path(user_id: int, db: Session = Depends(get_db)):
	user_model = db.query(models.Users).filter(models.Users.id == user_id).first()
	if user_model is not None:
		return user_model
	return 'Invalid user_id'


@router.get('/user/')
async def user_by_query(user_id: int, db: Session = Depends(get_db)):
	user_model = db.query(models.Users).filter(models.Users.id == user_id).first()
	if user_model is not None:
		return user_model
	return 'Invalid user_id'


@router.put('/user/change_password')
async def user_pass_change(user_verification: schemas.UserVerification, user: dict = Depends(get_current_user),
						   db: Session = Depends(get_db)):
	if user is None:
		raise get_user_exception()

	user_model = db.query(models.Users).filter(models.Users.id == user.get('id')).first()
	if user_model is not None:
		if user_verification.username == user_model.username and verify_password(
			user_verification.password, hashed=user_model.hpass):

			user_model.hpass = get_password_hash(user_verification.new_password)
			db.add(user_model)
			db.commit()

			return 'Successful'
		return 'Invalid user or request'


@router.delete('/user/')
async def delete_user(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
	if user is None:
		raise get_user_exception()

	user_model = db.query(models.Users).filter(models.Users.id == user.get('id')).first()
	if user_model is None:
		return 'Invalid user or request'

	db.query(models.Users).filter(models.Users.id == user.get('id')).delete()
	db.commit()

	return 'Delete Successful'
