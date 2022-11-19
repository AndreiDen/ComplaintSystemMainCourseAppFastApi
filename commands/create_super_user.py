from pprint import pprint

import asyncclick as click

from managers.user import UserManager
from models import RoleType
from db import database
from schemas.request.user import UserRegisterIn


class SuperUser:
    def dict(self):
        return self.__dict__

@click.command()
@click.option("-f", "--first_name", type=str, required=True)
@click.option("-l", "--last_name", type=str, required=True)
@click.option("-e", "--email", type=str, required=True)
@click.option("-p", "--phone", type=str, required=True)
@click.option("-i", "--iban", type=str, required=True)
@click.option("-pa", "--password", type=str, required=True)
async def create_user(first_name, last_name, email, phone, iban, password):
    user_data = SuperUser()
    user_data.email = email
    user_data.first_name = first_name
    user_data.last_name = last_name
    user_data.phone = phone
    user_data.iban = iban
    user_data.password = password
    await database.connect()
    await UserManager.register(user_data=user_data)
    await database.disconnect()

if __name__ == "__main__":
    create_user(_anyio_backend="asyncio")
