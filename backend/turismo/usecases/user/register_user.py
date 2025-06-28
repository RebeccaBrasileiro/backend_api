from turismo.domain.entities.user import User
from turismo.domain.repositories.user_repository import UserRepository


class RegisterUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self, user: User) -> User:
        return self.repository.register(user)