from typing import Dict, List
from fastapi import APIRouter, Request

from endpoints.models import Oferta, SemanticSearchTerms, OfertasHistory
from endpoints import service

router = APIRouter()

@router.post("/addOferta")
async def addOferta(request: Request, oferta: Oferta) -> Dict:
    if service.addOferta(oferta.__dict__, request.app.state.ofertasCollection, request.app.state.transformerModel, request.app.state.nonindexed):
        request.app.state.nonindexed = 0

    return {"status": "success"}

@router.get("/getOferta/{ofertaid}")
async def getOferta(request: Request, ofertaid: str) -> Dict:
    res = service.getOferta({"ofertaid": ofertaid}, request.app.state.ofertasCollection)

    res["oferta"] = [float(i) for i in res["oferta"]]

    return res

@router.get("/deleteOferta/{ofertaid}")
async def deleteOferta(request: Request, ofertaid: str) -> Dict:
    if not service.deleteOferta({"ofertaid": ofertaid}, request.app.state.ofertasCollection):
        return {"status": "failed"}

    return {"status": "success"}

@router.post("/semanticSearch")
async def semanticSearch(request: Request, search_terms: SemanticSearchTerms) -> List:
    res = service.semanticSearch(search_terms.search_term, search_terms.category, search_terms.region, request.app.state.ofertasCollection, request.app.state.transformerModel)

    return res

@router.post("/recommendOfertas")
async def recommendOfertas(request: Request, history: OfertasHistory):
    pass
