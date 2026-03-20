import graphene


class BackgroundFeatureType(graphene.ObjectType):
    name = graphene.String(required=True)
    description = graphene.String(required=True)


class BackgroundType(graphene.ObjectType):
    id = graphene.ID(required=True)
    name = graphene.String(required=True)
    edition = graphene.String(required=True)
    description = graphene.String()
    skill_proficiencies = graphene.List(graphene.NonNull(graphene.String))
    tool_proficiencies = graphene.List(graphene.NonNull(graphene.String))
    languages = graphene.List(graphene.NonNull(graphene.String))
    equipment = graphene.String()
    feature = graphene.Field(BackgroundFeatureType)
