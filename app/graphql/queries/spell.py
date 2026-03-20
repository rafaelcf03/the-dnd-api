import graphene

from app.graphql.types import SpellType
from app.models.spell import Spell


def _to_type(doc: Spell) -> SpellType:
    data = doc.model_dump()
    data["id"] = str(doc.id)
    return SpellType(**data)


class SpellQuery:
    spells = graphene.List(
        graphene.NonNull(SpellType),
        name=graphene.String(),
        level=graphene.Int(),
        school=graphene.String(),
        class_name=graphene.String(name="className"),
        description="List spells with optional filters.",
    )
    spell = graphene.Field(
        SpellType,
        id=graphene.ID(required=True),
        description="Get a single spell by ID.",
    )

    @staticmethod
    async def resolve_spells(
        root,
        info,
        name: str | None = None,
        level: int | None = None,
        school: str | None = None,
        class_name: str | None = None,
    ):
        edition = info.context["edition"]
        query: dict = {"edition": edition}
        if name:
            query["name"] = {"$regex": name, "$options": "i"}
        if level is not None:
            query["level"] = level
        if school:
            query["school"] = {"$regex": school, "$options": "i"}
        if class_name:
            query["classes"] = {"$regex": class_name, "$options": "i"}
        docs = await Spell.find(query).sort("level", "name").to_list()
        return [_to_type(d) for d in docs]

    @staticmethod
    async def resolve_spell(root, info, id: str):
        doc = await Spell.get(id)
        if doc and doc.edition == info.context["edition"]:
            return _to_type(doc)
        return None
