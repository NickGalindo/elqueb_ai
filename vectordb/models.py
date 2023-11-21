from pymilvus import DataType, FieldSchema, CollectionSchema

ofertaid = FieldSchema(
    name="ofertaid",
    dtype=DataType.VARCHAR,
    max_length=200,
    is_primary=True,
)

oferta = FieldSchema(
    name="oferta",
    dtype=DataType.FLOAT_VECTOR,
    dim=1024,
)

category = FieldSchema(
    name="category",
    dtype=DataType.VARCHAR,
    max_length=50
)

region = FieldSchema(
    name="region",
    dtype=DataType.VARCHAR,
    max_length="20"
)

schema = CollectionSchema(
    fields=[ofertaid, oferta, category, region],
    description="Ofertas Collection for semantic search"
)
