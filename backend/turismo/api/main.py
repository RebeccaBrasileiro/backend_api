from fastapi import FastAPI
from fastapi.security import HTTPBearer
from turismo.api.routes import comment_route, user_route
from turismo.api.openapi_tags import openapi_tags
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Turismo API",
    description="API backend do Site Turismo com Clean Architecture, FastAPI e PostgreSQL",
    version="1.0.0",
    contact={"name": "Maria Eduarda e Rebecca", "email": "turismo@exemplo.com"},
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
    openapi_tags=openapi_tags,
)

origins = [
    "http://localhost:5173",  # Vite local
    "https://frontclean.vercel.app",  # Produção
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # lista de origens confiáveis
    allow_credentials=True,
    allow_methods=["*"],  # ou especifique ["GET", "POST"]
    allow_headers=["*"],
)


@app.get("/")
def ola():
    return {"olá": "fastapi"}


app.include_router(user_route.router, prefix="/users", tags=["Users"])
app.include_router(comment_route.router, prefix="/comments", tags=["Comments"])
