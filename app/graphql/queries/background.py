import graphene

from app.graphql.types import BackgroundType
from app.models.background import Background


def _to_type(doc: Background) -> BackgroundType:
    data = doc.model_dump()
    data["id"] = str(doc.id)
    return BackgroundType(**data)


class BackgroundQuery:
    backgrounds = graphene.List(
        graphene.NonNull(BackgroundType),
        name=graphene.String(),
        description="List backgrounds, optionally filtered by name.",
    )
    background = graphene.Field(
        BackgroundType,
        id=graphene.ID(required=True),
        description="Get a single background by ID.",
    )

    @staticmethod
    async def resolve_backgrounds(root, info, name: str | None = None):
        edition = info.context["edition"]
        query = {"edition": edition}
        if name:
            query["name"] = {"$regex": name, "$options": "i"}
        docs = await Background.find(query).sort("name").to_list()
        return [_to_type(d) for d in docs]

    @staticmethod
    async def resolve_background(root, info, id: str):
        doc = await Background.get(id)
        if doc and doc.edition == info.context["edition"]:
            return _to_type(doc)
        return None
