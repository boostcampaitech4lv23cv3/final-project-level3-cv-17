from ..db_models.user import users
from ..db_config.db import conn
from fastapi import APIRouter
from ..schemas.user import User

user = APIRouter(prefix="/users")


@user.get('/users_table')
def fetch_all():
    return conn.execute(users.select()).fetchall()
# select

@user.get('/{name},{password}')
def get_name(name : str, password: str):
    return conn.execute(users.select().where(users.c.name == name and users.c.password == password)).first()
# select

@user.post('/')
def create_user(user: User):
   conn.execute(users.insert().values(name=user.name,
                email=user.email, password=user.password))
   return conn.execute(users.select()).fetchall()
# create


@user.put('/{id}')
def update_user(user: User, id: int):
    conn.execute(users.update().values(name=user.name, email=user.email,
                 password=user.password).where(users.c.id == id))
    return conn.execute(users.select().where(users.c.id == id)).first()
# update


@user.delete('/{id}')
def delete_user(id: int):
    conn.execute(users.delete().where(users.c.id == id))
    return conn.execute(users.select().where(users.c.id == id)).first()
#delete