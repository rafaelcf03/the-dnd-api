from beanie import Document, Indexed
from pydantic import BaseModel, Field


class BackgroundFeature(BaseModel):
    name: str
    description: str


class Background(Document):
    name: Indexed(str)  # type: ignore[valid-type]
    edition: Indexed(str)  # type: ignore[valid-type]
    description: str = ""
    skill_proficiencies: list[str] = Field(default_factory=list)
    tool_proficiencies: list[str] = Field(default_factory=list)
    languages: list[str] = Field(default_factory=list)
    equipment: str = ""
    feature: BackgroundFeature | None = None

    class Settings:
        name = "backgrounds"
        indexes = [("name", "edition")]
