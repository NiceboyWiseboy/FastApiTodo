from typing import Optional
from pydantic import BaseModel, Field


class Todo(BaseModel):
	title: str
	description: Optional[str]
	priority: int = Field(gt=0, lt=6, description='Priority must be between 1-5')
	complete: bool

	class Config:
		orm_mode = True


class CreateUser(BaseModel):
	username: str
	email: Optional[str]
	fname: str
	lname: str
	password: str


class UserVerification(BaseModel):
	username: str
	password: str
	new_password: str
