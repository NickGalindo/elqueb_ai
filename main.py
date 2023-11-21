from manager.load_config import CONFIG

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

import pymilvus

import colorama 
from colorama import Fore

from sentence_transformers import SentenceTransformer

from vectordb.setupCollections import setupCollection
from endpoints import router as endpoints_router

colorama.init(autoreset=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.milvusConnection = pymilvus.connections.connect(
        alias=CONFIG["VDB_ALIAS"],
        host=CONFIG["VDB_HOST"],
        port=CONFIG["VDB_PORT"]
    )

    app.state.ofertasCollection = setupCollection()

    app.state.transformerModel = SentenceTransformer(CONFIG["TRANSFORMER_MODEL"])

    app.state.nonindexed = 0

    yield

    if not pymilvus.connections.has_connection(CONFIG["VDB_ALIAS"]):
        return

    app.state.ofertasCollection.flush()
    app.state.ofertasCollection.release()

    pymilvus.connections.disconnect(CONFIG["VDB_ALIAS"])


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(endpoints_router)
