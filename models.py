from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base, engine


class Users(Base):
	Base.metadata.create_all(bind=engine)

	__tablename__ = 'users'
	id = Column(Integer, primary_key=True, index=True)
	email = Column(String, unique=True, index=True)
	username = Column(String, unique=True, index=True)
	fname = Column(String)
	lname = Column(String)
	hpass = Column(String)
	is_active = Column(Boolean, default=True)
	phone_number = Column(String)
	address_id = Column(Integer, ForeignKey('address.id'), nullable=True)

	todos = relationship('Todos', back_populates='owner')
	address = relationship('Address', back_populates='user_address')


class Todos(Base):
	Base.metadata.create_all(bind=engine)

	__tablename__ = 'todos'
	id = Column(Integer, primary_key=True, index=True)
	title = Column(String)
	description = Column(String)
	priority = Column(Integer)
	complete = Column(Boolean, default=False)
	owner_id = Column(Integer, ForeignKey('users.id'))

	owner = relationship('Users', back_populates='todos')


class Address(Base):
	Base.metadata.create_all(bind=engine)

	__tablename__ = 'address'

	id = Column(Integer, primary_key=True, index=True)
	address1 = Column(String)
	address2 = Column(String)
	city = Column(String)
	state = Column(String)
	country = Column(String)
	postal_code = Column(String)
	apt_num = Column(Integer)

	user_address = relationship('Users', back_populates='address')
