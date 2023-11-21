from typing import Dict, List

from manager.load_config import CONFIG

import re
import numpy as np

from pymilvus import Collection 
from sentence_transformers import SentenceTransformer

from vectordb.transform import transform

def __checkExistence(oferta: Dict, col: Collection):
    res = col.query(
        expr = f"ofertaid == \"{oferta['ofertaid']}\"",
        offset=0,
        limit=1,
        output_fields=["ofertaid", "oferta", "category", "region"],
        consistency_level="Strong"
    )

    if len(res) > 0:
        return res

    return None

def addOferta(oferta: Dict, col: Collection, model: SentenceTransformer, nonindexed: int) -> bool:
    if __checkExistence(oferta, col):
        return False

    oferta_vector: List = transform(oferta["oferta"], model).flatten().tolist()

    new_oferta: List = [
        [oferta["ofertaid"]],
        [oferta_vector],
        [oferta["category"]],
        [oferta["region"]]
    ]

    col.insert(new_oferta)

    if nonindexed >= CONFIG["INDEX_FRECUENCY"]:
        col.flush()
        return True
    else:
        return False

def getOferta(oferta: Dict, col: Collection) -> Dict:
    res = __checkExistence(oferta, col)

    if not res:
        return {}

    res = res[-1]

    assert(isinstance(res, Dict))

    return res

def deleteOferta(oferta: Dict, col: Collection) -> bool:
    res = __checkExistence(oferta, col)

    if not res:
        return False

    aux_res = col.delete(expr=f"ofertaid in [\"{oferta['ofertaid']}\"]")

    if not aux_res:
        return False

    return True

def editOferta(oferta: Dict, col: Collection, model: SentenceTransformer, nonindexed: int) -> bool:
    if not deleteOferta(oferta, col):
        return False

    return addOferta(oferta, col, model, nonindexed)

def semanticSearch(search_term: str, category: str | None, region: str | None, col: Collection, model: SentenceTransformer):
    embedding: List = transform(search_term, model).flatten().tolist()

    search_params: Dict = {"metric_type": "L2", "params": {"nprobe": 10}}

    filters = ""

    if category is not None:
        filters = f"category in [\"{category}\"]"

    if region is not None:
        if category is not None:
            filters += " && "
        filters += f"region in [\"{region}\"]"

    if region is not None or category is not None:
        res = col.search(
            data=[embedding],
            anns_field="oferta",
            param=search_params,
            limit=20,
            expr=filters
        )

        search_res = set()
        for aux in res: #type: ignore
            for entity in aux:
                search_res.add(entity.id)

        return list(search_res)

    res = col.search(
        data=[embedding],
        anns_field="oferta",
        param=search_params,
        limit=20
    )

    search_res = set()
    for aux in res: #type: ignore
        for entity in aux:
            search_res.add(entity.id)

    return list(search_res)
