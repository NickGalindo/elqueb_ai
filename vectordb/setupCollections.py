from typing import Dict, Tuple
from manager.load_config import CONFIG

from pymilvus import Collection, utility

from vectordb.models import schema

def setupCollection() -> Collection:
    index_params: Dict = {
        "metric_type": "L2",
        "index_type": "IVF_SQ8",
        "params":{"nlist": 1024}
    }

    if not utility.has_collection("Ofertas"):
        col = Collection(
            name="Ofertas",
            schema=schema,
            using=CONFIG["VDB_ALIAS"]
        )
        col.create_index(field_name="oferta", index_params=index_params)
    else:
        col = Collection("Ofertas")

    col.load()

    return col
