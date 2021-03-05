import graphene
import memories.schema


class Query(memories.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
