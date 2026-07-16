from backend.core.database import engine
from backend.core.configs import DBBaseModel
from backend.core.logging_config import config_logging
from backend.models.__all_models import *
#import logging

#config_logging()

#logger = logging.getLogger(__name__)

async def criar_tabelas():
    async with engine.begin() as conn:
        await conn.run_sync(DBBaseModel.metadata.create_all)

    #logger.info("Tabelas criadas com sucesso")

if __name__ == "__main__":
    import asyncio

    asyncio.run(criar_tabelas())