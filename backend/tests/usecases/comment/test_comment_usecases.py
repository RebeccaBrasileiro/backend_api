import uuid
import pytest
from turismo.domain.entities.comment import Comment
from turismo.infra.repositories.in_memory.in_memory_comment_repository import (
    InMemoryCommentRepository,
)
from turismo.usecases.comment.add_comment import AddCommentUseCase
from turismo.usecases.comment.delete_comment import DeleteCommentUseCase
from turismo.usecases.comment.get_comments_by_post import GetCommentsByPostUseCase
from turismo.usecases.comment.get_comments_by_user import GetCommentsByUserUseCase


def create_test_comment(user_id=None, post_id=None) -> Comment:
    return Comment(
        id=str(uuid.uuid4()),
        post_id=post_id or str(uuid.uuid4()),
        user_id=user_id or str(uuid.uuid4()),
        comment="Comentário de teste",
        date="2025-06-09",
    )


@pytest.mark.asyncio
async def test_add_comment():
    repo = InMemoryCommentRepository()
    comment = create_test_comment()
    usecase = AddCommentUseCase(repo)

    result = await usecase.execute(comment)

    assert result == comment
    assert repo._comments[comment.id] == comment


@pytest.mark.asyncio
async def test_get_comments_by_post():
    repo = InMemoryCommentRepository()
    post_id = str(uuid.uuid4())
    comment1 = create_test_comment(post_id=post_id)
    comment2 = create_test_comment(post_id=post_id)
    comment_other = create_test_comment()

    await repo.add_comment(comment1)
    await repo.add_comment(comment2)
    await repo.add_comment(comment_other)

    usecase = GetCommentsByPostUseCase(repo)
    result = await usecase.execute(post_id)

    assert comment1 in result
    assert comment2 in result
    assert comment_other not in result
    assert len(result) == 2


@pytest.mark.asyncio
async def test_get_comments_by_post_empty():
    repo = InMemoryCommentRepository()
    usecase = GetCommentsByPostUseCase(repo)
    result = await usecase.execute("post-vazio")

    assert result == []


@pytest.mark.asyncio
async def test_get_comments_by_user():
    repo = InMemoryCommentRepository()
    user_id = str(uuid.uuid4())
    comment1 = create_test_comment(user_id=user_id)
    comment2 = create_test_comment(user_id=user_id)
    comment_other = create_test_comment()

    await repo.add_comment(comment1)
    await repo.add_comment(comment2)
    await repo.add_comment(comment_other)

    usecase = GetCommentsByUserUseCase(repo)
    result = await usecase.execute(user_id)

    assert comment1 in result
    assert comment2 in result
    assert comment_other not in result
    assert len(result) == 2


@pytest.mark.asyncio
async def test_get_comments_by_user_empty():
    repo = InMemoryCommentRepository()
    usecase = GetCommentsByUserUseCase(repo)
    result = await usecase.execute("user-vazio")

    assert result == []


@pytest.mark.asyncio
async def test_delete_comment():
    repo = InMemoryCommentRepository()
    comment = create_test_comment()
    await repo.add_comment(comment)

    usecase = DeleteCommentUseCase(repo)
    await usecase.execute(comment.id)

    assert comment.id not in repo._comments


@pytest.mark.asyncio
async def test_delete_comment_not_found():
    repo = InMemoryCommentRepository()
    usecase = DeleteCommentUseCase(repo)

    # Só garante que não levanta erro
    await usecase.execute("id-invalido")
