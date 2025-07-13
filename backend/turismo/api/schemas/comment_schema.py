from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from turismo.api.schemas.user_schema import UserOutput
from turismo.domain.entities.comment import Comment
from turismo.api.schemas.user_schema import user_to_output


class AddCommentInput(BaseModel):
    post_id: str = Field(
        ..., description="ID do post ao qual o comentário será adicionado"
    )
    comment: str = Field(
        ..., min_length=1, max_length=500, description="Texto do comentário"
    )
    date: datetime = Field(..., description="Data do comentário no formato ISO 8601")


class CommentOutput(BaseModel):
    id: str = Field(..., description="ID do comentário")
    post_id: str = Field(..., description="ID do post ao qual o comentário pertence")
    user_id: str = Field(..., description="ID do usuário que fez o comentário")
    comment: str = Field(
        ..., min_length=1, max_length=500, description="Texto do comentário"
    )
    date: datetime = Field(..., description="Data do comentário no formato ISO 8601")
    user: UserOutput = Field(..., description="Dados do usuário que está postando")

    @classmethod
    def from_entity(cls, comment):
        return cls(
            id=comment.id,
            post_id=comment.post_id,
            user_id=comment.user_id,
            comment=comment.comment,
            date=comment.date,
            user=comment.user,
        )


def comment_to_output(comment: Comment) -> CommentOutput:
    return CommentOutput(
        id=comment.id,
        post_id=comment.post_id,
        user_id=comment.user_id,
        comment=comment.comment,
        date=comment.date,
        user=user_to_output(comment.user) if comment.user else None,
    )


def comments_to_output(comments: list[Comment]) -> list[CommentOutput]:
    return [comment_to_output(comment) for comment in comments]
