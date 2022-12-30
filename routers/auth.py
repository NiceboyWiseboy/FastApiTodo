import sys
sys.path.append('..')
import models
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt
from fastapi import Depends, HTTPException, status, APIRouter
from database import SessionLocal
from schemas import CreateUser
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer


router = APIRouter(
	prefix='/auth',
	tags=['auth'],
	responses={401: {'user': 'Not Authorized'}}
)
SECRET_KEY = 'qwertyuiopasdfghjklzxcvbnm1234567890'
ALGORITHM = 'HS256'
outh2_bearer = OAuth2PasswordBearer(tokenUrl='token')


def get_db():
	try:
		db = SessionLocal()
		yield db
	finally:
		db.close()


def get_password_hash(password):
	bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
	return bcrypt_context.hash(password)


def verify_password(plain, hashed):
	bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
	return bcrypt_context.verify(plain, hash=hashed)


def authenticate_user(username: str, password: str, db):
	user = db.query(models.Users).filter(models.Users.username == username).first()

	if not user:
		return False
	if not verify_password(password, user.hpass):
		return False

	return user


def create_access_token(username: str, user_id: int, expires_delta: Optional[timedelta] = None):
	encode = {'sub': username, 'id': user_id}
	if expires_delta:
		expire = datetime.utcnow() + expires_delta
	else:
		expire = datetime.utcnow() + timedelta(minutes=15)

	encode.update({'exp': expire})

	return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)



async def get_current_user(token: str = Depends(outh2_bearer)):
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		username: str = payload.get('sub')
		id: int = payload.get('id')

		if username is None or id is None:
			raise get_user_exception()
		return {'username': username, 'id': id}
	except:
		raise get_user_exception()
@router.post('/create/user')
async def create_new_user(create_user: CreateUser, db: Session = Depends(get_db)):
	create_user_model = models.Users()
	create_user_model.username = create_user.username
	create_user_model.email = create_user.email
	create_user_model.fname = create_user.fname
	create_user_model.lname = create_user.lname
	create_user_model.phone_number = create_user.phone_number
	hpass = get_password_hash(create_user.password)
	create_user_model.hpass = hpass
	create_user_model.is_active = True

	db.add(create_user_model)
	db.commit()


@router.post('/token')
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
	user = authenticate_user(form_data.username, form_data.password, db=db)
	if not user:
		raise token_exception()

	token_expires = timedelta(minutes=20)
	token = create_access_token(user.username, user.id, expires_delta=token_expires)

	return {'token': token}


def get_user_exception():
	credentials_exception = HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail='Could not validate credentials',
		headers={'WWW-Authenticate': 'Bearer'},
	)
	return credentials_exception


def token_exception():
	token_exception_resp = HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail='Incorrect Username or Password',
		headers={'WWW-Authenticate': 'Bearer'},
	)
	return token_exception_resp
