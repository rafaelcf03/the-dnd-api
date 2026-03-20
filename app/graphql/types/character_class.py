import graphene


class ClassFeatureType(graphene.ObjectType):
    name = graphene.String(required=True)
    level = graphene.Int(required=True)
    description = graphene.String(required=True)


class SubclassType(graphene.ObjectType):
    name = graphene.String(required=True)
    description = graphene.String()
    features = graphene.List(graphene.NonNull(ClassFeatureType))


class CharacterClassType(graphene.ObjectType):
    id = graphene.ID(required=True)
    name = graphene.String(required=True)
    edition = graphene.String(required=True)
    description = graphene.String()
    hit_die = graphene.Int()
    primary_ability = graphene.String()
    saving_throws = graphene.List(graphene.NonNull(graphene.String))
    armor_proficiencies = graphene.List(graphene.NonNull(graphene.String))
    weapon_proficiencies = graphene.List(graphene.NonNull(graphene.String))
    tool_proficiencies = graphene.List(graphene.NonNull(graphene.String))
    features = graphene.List(graphene.NonNull(ClassFeatureType))
    subclasses = graphene.List(graphene.NonNull(SubclassType))
