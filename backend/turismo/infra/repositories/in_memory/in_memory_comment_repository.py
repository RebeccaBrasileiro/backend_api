from turismo.domain.repositories.comment_repository import CommentRepository
from turismo.domain.entities.comment import Comment
from typing import List, Optional
import pytest


class InMemoryCommentRepository(CommentRepository):
    def __init__(self):
        self._comments = {}

    @pytest.mark.asyncio
    async def get_comments_by_post(self, post_id: str) -> List[Comment]:
        return [c for c in self._comments.values() if c.post_id == post_id]

    @pytest.mark.asyncio
    async def get_comments_by_user(self, user_id: str) -> List[Comment]:
        return [c for c in self._comments.values() if c.user_id == user_id]

    @pytest.mark.asyncio
    async def add_comment(self, comment: Comment) -> Comment:
        self._comments[comment.id] = comment
        return comment

    @pytest.mark.asyncio
    async def delete_comment(self, comment_id: str) -> None:
        self._comments.pop(comment_id, None)
