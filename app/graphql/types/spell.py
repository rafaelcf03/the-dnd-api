import graphene


class SpellComponentsType(graphene.ObjectType):
    verbal = graphene.Boolean()
    somatic = graphene.Boolean()
    material = graphene.Boolean()
    material_description = graphene.String()


class SpellType(graphene.ObjectType):
    id = graphene.ID(required=True)
    name = graphene.String(required=True)
    edition = graphene.String(required=True)
    level = graphene.Int()
    school = graphene.String()
    casting_time = graphene.String()
    range = graphene.String()
    components = graphene.Field(SpellComponentsType)
    duration = graphene.String()
    concentration = graphene.Boolean()
    ritual = graphene.Boolean()
    description = graphene.String()
    higher_levels = graphene.String()
    classes = graphene.List(graphene.NonNull(graphene.String))
