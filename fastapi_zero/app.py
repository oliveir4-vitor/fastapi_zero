from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fastapi_zero.database import get_session
from fastapi_zero.models import User
from fastapi_zero.schema import (
    Message,
    UserList,
    UserPublic,
    UserSchema,
)

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return Message(message='Olá Mundo!!')


@app.post('/users', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_users(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            User.username == user.username or User.email == user.email
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                detail='User name already exists',
                status_code=HTTPStatus.CONFLICT,
            )
        elif db_user.email == user.email:
            raise HTTPException(
                detail='Email already exists', status_code=HTTPStatus.CONFLICT
            )

    db_user = User(
        username=user.username,
        email=user.email,
        password=user.password,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users', status_code=HTTPStatus.OK, response_model=UserList)
def read_users(
    limit: int = 10,
    offset: int = 0,
    session: Session = Depends(get_session)
):
    users = session.scalars(
        select(User)
        .limit(limit)
        .offset(offset)
    )

    return {'users': users}


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    try:
        db_user.username = user.username
        db_user.password = user.password
        db_user.email = user.email
        session.commit()
        session.refresh(db_user)

        return db_user

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or Email already exists',
        )


@app.delete(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=Message
)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user_db = session.scalar(
        select(User).where(User.id == user_id)
    )
    if not user_db:
        raise HTTPException(
            detail='Usuário não encontrado!',
            status_code=HTTPStatus.NOT_FOUND
        )

    session.delete(user_db)
    session.commit()

    return Message(message='User delete')


@app.get(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def read_user(
    user_id: int, session: Session = Depends(get_session)
):
    user_db = session.scalar(
        select(User).where(User.id == user_id)
    )
    if not user_db:
        raise HTTPException(
            detail='Usuário não encontrado!',
            status_code=HTTPStatus.NOT_FOUND
        )

    return user_db
