from fastapi import APIRouter

api_router = APIRouter()

from backend.API.V1.endpoints import (
    user_route,
    fluxo_route,
    atendimento_route
)

api_router.include_router(
    user_route.router,
    prefix="/usuarios",
    tags=["Usuários"]
)

api_router.include_router(
    atendimento_route.router,
    prefix="/atendimentos",
    tags=["Atendimentos"]
)

api_router.include_router(
    fluxo_route.router,
    prefix="/fluxo",
    tags=["Fluxo de Triagem"]
)