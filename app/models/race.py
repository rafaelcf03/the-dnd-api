from beanie import Document, Indexed
from pydantic import BaseModel, Field


class AbilityBonus(BaseModel):
    ability: str
    bonus: int


class Trait(BaseModel):
    name: str
    description: str


class Subrace(BaseModel):
    name: str
    description: str = ""
    ability_bonuses: list[AbilityBonus] = Field(default_factory=list)
    traits: list[Trait] = Field(default_factory=list)


class Race(Document):
    name: Indexed(str)  # type: ignore[valid-type]
    edition: Indexed(str)  # type: ignore[valid-type]
    description: str = ""
    speed: int = 30
    size: str = "Medium"
    ability_bonuses: list[AbilityBonus] = Field(default_factory=list)
    traits: list[Trait] = Field(default_factory=list)
    languages: list[str] = Field(default_factory=list)
    subraces: list[Subrace] = Field(default_factory=list)

    class Settings:
        name = "races"
        indexes = [("name", "edition")]
