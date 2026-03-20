import graphene


class FeatType(graphene.ObjectType):
    id = graphene.ID(required=True)
    name = graphene.String(required=True)
    edition = graphene.String(required=True)
    category = graphene.String()
    prerequisite = graphene.String()
    description = graphene.String()
    benefits = graphene.List(graphene.NonNull(graphene.String))
