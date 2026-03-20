import graphene


class AbilityBonusType(graphene.ObjectType):
    ability = graphene.String(required=True)
    bonus = graphene.Int(required=True)


class TraitType(graphene.ObjectType):
    name = graphene.String(required=True)
    description = graphene.String(required=True)


class SubraceType(graphene.ObjectType):
    name = graphene.String(required=True)
    description = graphene.String()
    ability_bonuses = graphene.List(graphene.NonNull(AbilityBonusType))
    traits = graphene.List(graphene.NonNull(TraitType))


class RaceType(graphene.ObjectType):
    id = graphene.ID(required=True)
    name = graphene.String(required=True)
    edition = graphene.String(required=True)
    description = graphene.String()
    speed = graphene.Int()
    size = graphene.String()
    ability_bonuses = graphene.List(graphene.NonNull(AbilityBonusType))
    traits = graphene.List(graphene.NonNull(TraitType))
    languages = graphene.List(graphene.NonNull(graphene.String))
    subraces = graphene.List(graphene.NonNull(SubraceType))
