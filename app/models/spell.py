from beanie import Document, Indexed
from pydantic import BaseModel, Field


class SpellComponents(BaseModel):
    verbal: bool = False
    somatic: bool = False
    material: bool = False
    material_description: str = ""


class Spell(Document):
    name: Indexed(str)  # type: ignore[valid-type]
    edition: Indexed(str)  # type: ignore[valid-type]
    level: int = 0  # 0 = cantrip
    school: str = ""
    casting_time: str = ""
    range: str = ""
    components: SpellComponents = Field(default_factory=SpellComponents)
    duration: str = ""
    concentration: bool = False
    ritual: bool = False
    description: str = ""
    higher_levels: str | None = ""
    classes: list[str] = Field(default_factory=list)

    class Settings:
        name = "spells"
        indexes = [("name", "edition"), "level", "school"]
