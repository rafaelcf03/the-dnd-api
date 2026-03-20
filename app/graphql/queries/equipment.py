import graphene

from app.graphql.types import EquipmentType
from app.models.equipment import Equipment


def _to_type(doc: Equipment) -> EquipmentType:
    data = doc.model_dump()
    data["id"] = str(doc.id)
    return EquipmentType(**data)


class EquipmentQuery:
    equipment_list = graphene.List(
        graphene.NonNull(EquipmentType),
        name=graphene.String(),
        category=graphene.String(),
        description="List equipment with optional filters.",
    )
    equipment_item = graphene.Field(
        EquipmentType,
        id=graphene.ID(required=True),
        description="Get a single equipment item by ID.",
    )

    @staticmethod
    async def resolve_equipment_list(
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
        docs = await Equipment.find(query).sort("category", "name").to_list()
        return [_to_type(d) for d in docs]

    @staticmethod
    async def resolve_equipment_item(root, info, id: str):
        doc = await Equipment.get(id)
        if doc and doc.edition == info.context["edition"]:
            return _to_type(doc)
        return None
