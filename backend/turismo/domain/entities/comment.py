from datetime import datetime
from typing import Optional
from turismo.domain.entities.user import User


class Comment:
    def __init__(
        self,
        id: str,
        post_id: str,
        user_id: str,
        comment: str,
        date: datetime,
        user: Optional[User] = None,
    ):
        self.id = id
        self.post_id = post_id
        self.user_id = user_id
        self.comment = comment
        self.date = date
        self.user = user
