from backend.core.database import engine
from backend.core.configs import DBBaseModel

# IMPORTANTE:
# Isso importa todos os models para o SQLAlchemy registrar as tabelas
from backend.models.__all_models import *


async def criar_tabelas():
    async with engine.begin() as conn:
        await conn.run_sync(DBBaseModel.metadata.create_all)

    print('Tabelas criadas com sucesso')

if __name__ == "__main__":
    import asyncio

    asyncio.run(criar_tabelas())