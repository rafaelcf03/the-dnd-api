from beanie import Document, Indexed
from pydantic import BaseModel, Field


class ClassFeature(BaseModel):
    name: str
    level: int
    description: str


class Subclass(BaseModel):
    name: str
    description: str = ""
    features: list[ClassFeature] = Field(default_factory=list)


class CharacterClass(Document):
    name: Indexed(str)  # type: ignore[valid-type]
    edition: Indexed(str)  # type: ignore[valid-type]
    description: str = ""
    hit_die: int = 8
    primary_ability: str = ""
    saving_throws: list[str] = Field(default_factory=list)
    armor_proficiencies: list[str] = Field(default_factory=list)
    weapon_proficiencies: list[str] = Field(default_factory=list)
    tool_proficiencies: list[str] = Field(default_factory=list)
    features: list[ClassFeature] = Field(default_factory=list)
    subclasses: list[Subclass] = Field(default_factory=list)

    class Settings:
        name = "classes"
        indexes = [("name", "edition")]
