from typing import List
from sentence_transformers import SentenceTransformer
from manager.load_config import CONFIG
from torch import Tensor
from numpy import ndarray

def transform(sentence: str, model: SentenceTransformer) -> Tensor:
    res: List[Tensor] | ndarray | Tensor = model.encode(sentence, convert_to_tensor=True)
    assert(isinstance(res, Tensor))

    return res
