import models
from schemas import Todo
from fastapi import FastAPI, Depends, HTTPException
from database import engine, SessionLocal
from sqlalchemy.orm import Session


app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get('/')
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.Todos).all()


@app.get('/todo/{todo_id}')
async def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()

    if todo_model is not None:
        return todo_model
    raise not_found_exception()


@app.post('/')
async def create_todo(todo: Todo, db: Session = Depends(get_db)):
    todo_model = Todo()
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete

    db.add(todo_model)
    db.commit()

    successful_response(201)


@app.put('/todo/{todo_id}')
async def read_todo(todo_id: int, todo: Todo, db: Session = Depends(get_db)):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()

    if todo_model is None:
        raise not_found_exception()

    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete

    db.add(todo_model)
    db.commit()

    successful_response(200)


@app.delete('/todo/{todo_id}')
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()

    if todo_model is None:
        raise not_found_exception()

    db.query(Todo).filter(models.Todos.id == todo_id).delete()
    db.commit()

    successful_response(200)


def successful_response(status_code: int):
    return {
        'status': status_code,
        'transaction': 'Successful'
    }


def not_found_exception():
    return HTTPException(status_code=404, detail='Todo not found!!')
