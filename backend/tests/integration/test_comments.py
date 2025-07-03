import pytest
import datetime
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_and_get_comments(client: AsyncClient):
    # 1. Registro do usuário
    await client.post(
        "/users/register/",
        json={
            "name": "Comentador",
            "email": "comment@example.com",
            "password": "test@Comment123",
            "role": "user",
        },
    )

    # 2. Login
    login_response = await client.post(
        "/users/login/",
        json={"email": "comment@example.com", "password": "test@Comment123"},
    )
    print(login_response)
    token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    # 3. Criação de post para comentar
    post_response = await client.post(
        "/posts/",
        json={
            "title": "Post para Comentário",
            "description": "Desc",
            "content": "Conteúdo do post",
            "date": datetime.datetime.now().isoformat(),
        },
        headers=headers,
    )
    assert post_response.status_code == 200
    post_id = post_response.json()["id"]

    # 4. Criar comentário
    comment_response = await client.post(
        "/comments/",
        json={"post_id": post_id, "content": "Primeiro comentário!"},
        headers=headers,
    )
    assert comment_response.status_code == 200
    comment_data = comment_response.json()
    assert comment_data["content"] == "Primeiro comentário!"
    assert comment_data["post_id"] == post_id

    # 5. Buscar comentários por post
    list_response = await client.get(f"/comments/post/{post_id}", headers=headers)
    assert list_response.status_code == 200
    comments = list_response.json()
    assert any(c["content"] == "Primeiro comentário!" for c in comments)