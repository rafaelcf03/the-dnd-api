from beanie import Document, Indexed
from pydantic import Field


class Equipment(Document):
    name: Indexed(str)  # type: ignore[valid-type]
    edition: Indexed(str)  # type: ignore[valid-type]
    category: str = ""  # weapon, armor, adventuring_gear, tool
    cost: str = ""
    weight: str = ""
    description: str = ""
    properties: dict = Field(default_factory=dict)

    class Settings:
        name = "equipment"
        indexes = [("name", "edition"), "category"]
