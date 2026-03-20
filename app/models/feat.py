from beanie import Document, Indexed
from pydantic import Field


class Feat(Document):
    name: Indexed(str)  # type: ignore[valid-type]
    edition: Indexed(str)  # type: ignore[valid-type]
    category: str = "General"  # Origin, General, Fighting Style, Epic Boon
    prerequisite: str = ""
    description: str = ""
    benefits: list[str] = Field(default_factory=list)

    class Settings:
        name = "feats"
        indexes = [("name", "edition"), "category"]
