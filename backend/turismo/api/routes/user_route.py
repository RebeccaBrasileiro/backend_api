from fastapi import APIRouter, HTTPException, Depends
from turismo.usecases.user.register_user import RegisterUserUseCase
from turismo.usecases.user.login_user import LoginUserUseCase
from turismo.usecases.user.logout_user import LogoutUserUseCase
from turismo.usecases.user.get_current_user import GetCurrentUserUseCase
from turismo.domain.entities.user import User
from turismo.domain.value_objects.email_vo import Email
from turismo.domain.value_objects.password import Password, PasswordValidationError
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from turismo.api.deps import get_db_session, get_user_repository, get_current_user
from turismo.infra.repositories.sqlalchemy.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from turismo.api.schemas.user_schema import (
    RegisterUserInput,
    UserOutput,
    MessageUserResponse,
)
from turismo.api.schemas.token_schema import TokenResponse
from turismo.api.security import create_access_token
from turismo.domain.repositories.user_repository import UserRepository
from turismo.api.schemas.user_schema import LoginUserInput
from turismo.api.security import verify_token

security = HTTPBearer()
router = APIRouter()

# ----------------------
# Register
# ----------------------


@router.post(
    "/register",
    response_model=MessageUserResponse,
    summary="Registrar novo usuário",
    description="Cria um novo usuário com nome, email e senha forte.",
)
async def register_user(
    data: RegisterUserInput, db: AsyncSession = Depends(get_db_session)
):
    try:
        user_repo = SQLAlchemyUserRepository(db)
        usecase = RegisterUserUseCase(user_repo)
        user = User(
            id=str(uuid.uuid4()),
            name=data.name,
            email=Email(data.email),
            password=Password(data.password),
            role=data.role,
        )
        result = await usecase.execute(user)
        return MessageUserResponse(
            message="User registered successfully", user=UserOutput.from_entity(result)
        )
    except PasswordValidationError as p:
        raise HTTPException(status_code=400, detail=str(p))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ----------------------
# Login
# ----------------------


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Fazer o Login do usuário",
    description="Autentica um usuário com email e senha forte.",
)
async def login_user(
    data: LoginUserInput,
    user_repo: UserRepository = Depends(get_user_repository),
):
    try:
        usecase = LoginUserUseCase(user_repo)
        user = await usecase.execute(Email(data.email), Password(data.password))
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token = create_access_token(data={"sub": user.id})
        return TokenResponse(access_token=token, token_type="bearer")
    except PasswordValidationError as p:
        raise HTTPException(status_code=400, detail=str(p))
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


# ----------------------
# Get Current User
# ----------------------


@router.get(
    "/me",
    response_model=UserOutput,
    summary="Informar os dados do usuário atual",
    description="Retorna os dados do usuário atual.",
)
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user_repo: UserRepository = Depends(get_user_repository),
    user: str = Depends(get_current_user),
):
    try:
        usecase = GetCurrentUserUseCase(user_repo)
        result = await usecase.execute(user.id)
        return {
            "id": result.id,
            "name": result.name,
            "email": str(result.email),
            "role": result.role,
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))