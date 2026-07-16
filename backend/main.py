from backend.core.logging_config import config_logging


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.API.api_router import api_router


app = FastAPI(
    title="Sistema de Triagem Médica",
    description="""
API responsável por gerenciamento de usuários,
atendimentos e fluxo de triagem automatizado.
""",
    version="1.0.0"
)

# ==================== CORS ====================

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# ==================== ROTAS ====================

app.include_router(api_router)


# ==================== HEALTH CHECK ====================

@app.get(
    "/health",
    tags=["Health Check"]
)
async def health_check():
    return {
        "status": "online",
        "message": "API funcionando normalmente"
    }