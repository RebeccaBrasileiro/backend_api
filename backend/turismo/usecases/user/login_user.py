from turismo.domain.value_objects.email_vo import Email
from turismo.domain.value_objects.password import Password
from turismo.domain.entities.user import User
from turismo.domain.repositories.user_repository import UserRepository
from typing import Optional


class LoginUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, email: Email, password: Password) -> Optional[User]:
        return await self.repository.login(email, password)
