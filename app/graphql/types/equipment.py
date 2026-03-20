import graphene


class EquipmentType(graphene.ObjectType):
    id = graphene.ID(required=True)
    name = graphene.String(required=True)
    edition = graphene.String(required=True)
    category = graphene.String()
    cost = graphene.String()
    weight = graphene.String()
    description = graphene.String()
    properties = graphene.JSONString()
