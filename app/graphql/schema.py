import graphene

from app.graphql.queries.race import RaceQuery
from app.graphql.queries.character_class import CharacterClassQuery
from app.graphql.queries.spell import SpellQuery
from app.graphql.queries.background import BackgroundQuery
from app.graphql.queries.feat import FeatQuery
from app.graphql.queries.equipment import EquipmentQuery


class Query(
    graphene.ObjectType,
    RaceQuery,
    CharacterClassQuery,
    SpellQuery,
    BackgroundQuery,
    FeatQuery,
    EquipmentQuery,
):
    """Root query combining all D&D domain queries."""


schema = graphene.Schema(query=Query)
