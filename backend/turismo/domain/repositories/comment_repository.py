from abc import ABC, abstractmethod
from turismo.domain.entities.comment import Comment


class CommentRepository(ABC):
    @abstractmethod
    async def get_comments_by_post(self, post_id: str) -> list[Comment]: ...

    @abstractmethod
    async def get_comments_by_user(self, user_id: str) -> list[Comment]: ...

    @abstractmethod
    async def add_comment(self, comment: Comment) -> Comment: ...

    @abstractmethod
    async def delete_comment(self, comment_id: str) -> None: ...
