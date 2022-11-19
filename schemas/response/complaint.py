from datetime import datetime

from schemas.base import BaseComplaint


from models import State


class ComplaintOut(BaseComplaint):
    id: str
    status: State
    # complainer_id: str
    created_at: datetime


