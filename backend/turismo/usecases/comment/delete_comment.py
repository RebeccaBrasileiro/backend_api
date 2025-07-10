from turismo.domain.repositories.comment_repository import CommentRepository


class DeleteCommentUseCase:
    def __init__(self, repo):
        self.repo = repo

    async def execute(self, comment_id: str):
        await self.repo.delete_comment(comment_id)
