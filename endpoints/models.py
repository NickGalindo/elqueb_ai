from typing import List
from pydantic import BaseModel

class Oferta(BaseModel):
    ofertaid: str
    oferta: str
    category: str
    region: str

class SemanticSearchTerms(BaseModel):
    search_term: str
    category: str | None = None
    region: str | None = None

class OfertasHistory(BaseModel):
    history: List[str]
