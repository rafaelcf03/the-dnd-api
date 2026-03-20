import graphene

from app.graphql.types import FeatType
from app.models.feat import Feat


def _to_type(doc: Feat) -> FeatType:
    data = doc.model_dump()
    data["id"] = str(doc.id)
    return FeatType(**data)


class FeatQuery:
    feats = graphene.List(
        graphene.NonNull(FeatType),
        name=graphene.String(),
        category=graphene.String(),
        description="List feats with optional filters.",
    )
    feat = graphene.Field(
        FeatType,
        id=graphene.ID(required=True),
        description="Get a single feat by ID.",
    )

    @staticmethod
    async def resolve_feats(
        root,
        info,
        name: str | None = None,
        category: str | None = None,
    ):
        edition = info.context["edition"]
        query: dict = {"edition": edition}
        if name:
            query["name"] = {"$regex": name, "$options": "i"}
        if category:
            query["category"] = {"$regex": category, "$options": "i"}
        docs = await Feat.find(query).sort("category", "name").to_list()
        return [_to_type(d) for d in docs]

    @staticmethod
    async def resolve_feat(root, info, id: str):
        doc = await Feat.get(id)
        if doc and doc.edition == info.context["edition"]:
            return _to_type(doc)
        return None
