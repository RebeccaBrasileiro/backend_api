from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from turismo.domain.entities.comment import Comment
from turismo.domain.repositories.comment_repository import CommentRepository
from turismo.infra.models.comment_model import CommentModel
from sqlalchemy.orm import joinedload


class SQLAlchemyCommentRepository(CommentRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_comments_by_post(self, post_id: str) -> List[Comment]:
        result = await self._session.execute(
            select(CommentModel)
            .options(joinedload(CommentModel.user))
            .where(CommentModel.post_id == post_id)
        )
        return [c.to_entity() for c in result.unique().scalars().all()]

    async def get_comments_by_user(self, user_id: str) -> List[Comment]:
        result = await self._session.execute(
            select(CommentModel).where(CommentModel.user_id == user_id)
        )
        return [c.to_entity() for c in result.unique().scalars().all()]

    async def add_comment(self, comment: Comment) -> Comment:
        # Removida a verificação de existência de PostModel
        db_comment = CommentModel.from_entity(comment)
        self._session.add(db_comment)
        await self._session.commit()
        await self._session.refresh(db_comment)
        return db_comment.to_entity()

    async def delete_comment(self, comment_id: str) -> None:
        await self._session.execute(
            delete(CommentModel).where(CommentModel.id == comment_id)
        )
        await self._session.commit()
