from fastapi import APIRouter, Depends, status, HTTPException
# Сессия БД
from sqlalchemy.orm import Session
# Функция подключения к БД
from backend.db_depends import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from models import User
from schemas import CreateUser, UpdateUser
# Функции работы с записями.
from sqlalchemy import insert, select, update, delete
# Функция создания slug-строки
from slugify import slugify

router = APIRouter(prefix='/user', tags=['user'])
'''Напишите логику работы функций маршрутов:
Каждая из нижеперечисленных функций подключается к базе данных в момент обращения
при помощи функции get_db - Annotated[Session, Depends(get_db)]'''

'''Функция all_users ('/'):
Должна возвращать список всех пользователей из БД. Используйте scalars, select и all'''
@router.get('/')
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    if users is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no users'
        )
    return users

'''Функция user_by_id ('/user_id'):
Для извлечения записи используйте ранее импортированную функцию select.
Дополнительно принимает user_id.
Выбирает одного пользователя из БД.
Если пользователь не None, то возвращает его.
В противном случае выбрасывает исключение с кодом 404 и описанием "User was not found"'''
@router.get('/user_id')
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: str):
    user = db.scalars(select(User).where(User.id == user_id))
    if user is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )
    return user

'''Функция create_user ('/create'):
Для добавления используйте ранее импортированную функцию insert.
Дополнительно принимает модель CreateUser.
Подставляет в таблицу User запись значениями указанными в CreateUser.
В конце возвращает словарь {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}
Обработку исключения существующего пользователя по user_id или username можете сделать по желанию.'''
@router.post('/create')
async def create_user(db: Annotated[Session, Depends(get_db)], createuser: CreateUser):
        db.execute(insert(User).values(username=createuser.username,
                                       firstname=createuser.firstname,
                                       lastname=createuser.lastname,
                                       age=createuser.age,
                                       slug=slugify(createuser.username)
                                       ))
        db.commit()
        return {
            'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'
        }

'''Функция update_user ('/update'):
Для обновления используйте ранее импортированную функцию update.
Дополнительно принимает модель UpdateUser и user_id.
Если находит пользователя с user_id, то заменяет эту запись значениям из модели UpdateUser.
Далее возвращает словарь {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}
В противном случае выбрасывает исключение с кодом 404 и описанием "User was not found"'''
@router.put('/update')
async def update_user(db: Annotated[Session, Depends(get_db)], user_id: int,
                      update_user_model: UpdateUser):
    user_update = db.scalar(select(User).where(User.id == user_id))
    if user_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )

    db.execute(update(User).where(User.id == user_id)
               .values(firstname=update_user_model.firstname,
                       lastname=update_user_model.lastname,
                       age=update_user_model.age
                       #slug=slugify(update_user_model.lastname)
                       ))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User update is successful!'
    }

'''Функция delete_user ('/delete'):
Для удаления используйте ранее импортированную функцию delete.
Всё должно работать аналогично функции update_user, только объект удаляется.
Исключение выбрасывать то же.'''
@router.delete('/delete')
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    user_update = db.scalar(select(User).where(User.id == user_id))
    if user_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )

    db.execute(delete(User).where(User.id == user_id))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User was deleted successfully!'
    }