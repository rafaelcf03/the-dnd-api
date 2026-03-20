import graphene

from app.graphql.types import RaceType
from app.models.race import Race


def _to_type(doc: Race) -> RaceType:
    data = doc.model_dump()
    data["id"] = str(doc.id)
    return RaceType(**data)


class RaceQuery:
    races = graphene.List(
        graphene.NonNull(RaceType),
        name=graphene.String(),
        description="List races, optionally filtered by name.",
    )
    race = graphene.Field(
        RaceType,
        id=graphene.ID(required=True),
        description="Get a single race by ID.",
    )

    @staticmethod
    async def resolve_races(root, info, name: str | None = None):
        edition = info.context["edition"]
        query = {"edition": edition}
        if name:
            query["name"] = {"$regex": name, "$options": "i"}
        docs = await Race.find(query).sort("name").to_list()
        return [_to_type(d) for d in docs]

    @staticmethod
    async def resolve_race(root, info, id: str):
        doc = await Race.get(id)
        if doc and doc.edition == info.context["edition"]:
            return _to_type(doc)
        return None
