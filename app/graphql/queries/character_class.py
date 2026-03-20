import graphene

from app.graphql.types import CharacterClassType
from app.models.character_class import CharacterClass


def _to_type(doc: CharacterClass) -> CharacterClassType:
    data = doc.model_dump()
    data["id"] = str(doc.id)
    return CharacterClassType(**data)


class CharacterClassQuery:
    classes = graphene.List(
        graphene.NonNull(CharacterClassType),
        name=graphene.String(),
        description="List classes, optionally filtered by name.",
    )
    character_class = graphene.Field(
        CharacterClassType,
        id=graphene.ID(required=True),
        description="Get a single class by ID.",
    )

    @staticmethod
    async def resolve_classes(root, info, name: str | None = None):
        edition = info.context["edition"]
        query = {"edition": edition}
        if name:
            query["name"] = {"$regex": name, "$options": "i"}
        docs = await CharacterClass.find(query).sort("name").to_list()
        return [_to_type(d) for d in docs]

    @staticmethod
    async def resolve_character_class(root, info, id: str):
        doc = await CharacterClass.get(id)
        if doc and doc.edition == info.context["edition"]:
            return _to_type(doc)
        return None
