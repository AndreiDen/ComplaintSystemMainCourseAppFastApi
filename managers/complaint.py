from db import database
from models import complaints_table, RoleType, State


class ComplaintManager:
    @staticmethod
    async def get_complaints(user):
        _q = complaints_table.select()
        if user["role"] == RoleType.complainer:
            q = _q.where(complaints_table.c.complainer_id == user["id"])
        elif user["role"] == RoleType.approver:
            q = _q.where(complaints_table.c.status == State.pending)
        elif user["role"] == RoleType.admin:
            q = _q
        return await database.fetch_all(q)

    @staticmethod
    async def create_complaint(complaint_data, user):
        complaint_data.update({"complainer_id": user.id})
        id_ = await database.execute(complaints_table.insert().values(complaint_data))
        return await database.fetch_one(complaints_table.select().where(complaints_table.c.id == id_))

    @staticmethod
    async def delete_complaint(id_):
        await database.execute(complaints_table.delete().where(complaints_table.c.id == id_))

    @staticmethod
    async def approve_complaint(id_):
        await database.execute(complaints_table.update().where(complaints_table.c.id == id_).values(status=State.approved))

    @staticmethod
    async def reject_complaint(id_):
        await database.execute(complaints_table.update().where(complaints_table.c.id == id_).values(status=State.rejected))

