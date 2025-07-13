from turismo.domain.entities.comment import Comment
from turismo.domain.repositories.comment_repository import CommentRepository
from typing import Optional


class AddCommentUseCase:
    def __init__(self, repository: CommentRepository):
        self.repository = repository

    async def execute(self, comment: Comment) -> Optional[Comment]:
        return await self.repository.add_comment(comment)
