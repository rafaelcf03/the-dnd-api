from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings
from app.models.race import Race
from app.models.character_class import CharacterClass
from app.models.spell import Spell
from app.models.background import Background
from app.models.feat import Feat
from app.models.equipment import Equipment

ALL_MODELS = [Race, CharacterClass, Spell, Background, Feat, Equipment]

_client: AsyncIOMotorClient | None = None


async def init_db() -> None:
    global _client
    _client = AsyncIOMotorClient(settings.MONGO_URI)
    await init_beanie(
        database=_client[settings.MONGO_DB_NAME],
        document_models=ALL_MODELS,
    )


async def close_db() -> None:
    global _client
    if _client:
        _client.close()
        _client = None
