from pprint import pprint

from fastapi import HTTPException
from passlib.context import CryptContext
from asyncpg import UniqueViolationError
from db import database
from managers.auth import AuthManager
from models import users_table, RoleType

pwd_context = CryptContext(schemes=["bcrypt"],
                           deprecated="auto")


class UserManager:
    @staticmethod
    async def register(user_data):
        user_data.password = pwd_context.hash(user_data.password)
        try:
            q = users_table.insert().values(**user_data.dict())
            id_ = await database.execute(q)
        except UniqueViolationError:
            raise HTTPException(400, "User with this email already exists")
        user_do = await database.fetch_one(users_table.select(users_table.c.id == id_))
        # user_do - user database object

        return AuthManager.encode_token(user_do)

    @staticmethod
    async def login(user_data):
        user_do = await database.fetch_one(users_table.select().where(users_table.c.email == user_data.email))
        if not user_do:
            raise HTTPException(400, "Wrong email or password")
        elif not pwd_context.verify(user_data.password, user_do["password"]):
            raise HTTPException(400, "Wrong email or password")
        return AuthManager.encode_token(user_do)

    @staticmethod
    async def get_all_users():
        return await database.fetch_all(users_table.select())

    @staticmethod
    async def get_user_by_email(email):
        return await database.fetch_all(users_table.select().where(users_table.c.email == email))


    @staticmethod
    async def change_role(role: RoleType, user_id):
        await database.execute(users_table.update().where(users_table.c.id == user_id).values(role=role))





