from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from turismo.usecases.comment.add_comment import AddCommentUseCase
from turismo.usecases.comment.delete_comment import DeleteCommentUseCase
from turismo.usecases.comment.get_comments_by_post import GetCommentsByPostUseCase
from turismo.usecases.comment.get_comments_by_user import GetCommentsByUserUseCase
from turismo.domain.entities.comment import Comment
import uuid
from turismo.api.schemas.comment_schema import AddCommentInput, CommentOutput
from turismo.domain.repositories.comment_repository import CommentRepository
from sqlalchemy.ext.asyncio import AsyncSession
from turismo.api.deps import (
    get_db_session,
    get_user_repository,
    get_comment_repository,
    get_current_user,
)
from turismo.infra.repositories.sqlalchemy.sqlalchemy_comment_repository import (
    SQLAlchemyCommentRepository,
)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()
router = APIRouter()


@router.get("/post/{post_id}", response_model=List[CommentOutput])
async def get_comments_by_post(
    post_id: str, comment_repo: CommentRepository = Depends(get_comment_repository)
):
    usecase = GetCommentsByPostUseCase(comment_repo)
    comments = await usecase.execute(post_id)
    return comments


@router.get("/user", response_model=List[CommentOutput])
async def get_comments_by_user(
    comment_repo: CommentRepository = Depends(get_comment_repository),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user: str = Depends(get_current_user),
):
    usecase = GetCommentsByUserUseCase(comment_repo)
    comments = await usecase.execute(user.id)
    return comments


@router.post("/", response_model=CommentOutput)
async def add_comment(
    data: AddCommentInput,
    comment_repo: CommentRepository = Depends(get_comment_repository),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user: str = Depends(get_current_user),
):
    if data.date.tzinfo is not None:
        data.date = data.date.replace(tzinfo=None)
    comment = Comment(
        id=str(uuid.uuid4()),
        post_id=data.post_id,
        user_id=user.id,
        comment=data.comment,
        date=data.date,
    )
    usecase = AddCommentUseCase(comment_repo)
    added_comment = await usecase.execute(comment)
    return added_comment


@router.delete("/{comment_id}")
async def delete_comment(
    comment_id: str, comment_repo: CommentRepository = Depends(get_comment_repository)
):
    usecase = DeleteCommentUseCase(comment_repo)
    success = await usecase.execute(comment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Comment not found")
    return {"message": "Comment deleted successfully"}