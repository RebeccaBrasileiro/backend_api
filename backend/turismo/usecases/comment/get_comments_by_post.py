from turismo.domain.repositories.comment_repository import CommentRepository
from turismo.domain.entities.comment import Comment
from typing import List


class GetCommentsByPostUseCase:
    def __init__(self, repository: CommentRepository):
        self.repository = repository

    async def execute(self, post_id: str) -> List[Comment]:
        return await self.repository.get_comments_by_post(post_id)
