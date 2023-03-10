import json
import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware

# from spell_and_text.config.config import initiate_database, initiate_redis_pool
from spell_and_text.controllers.router import api_router
from spell_and_text.utils.logger import get_logger
from spell_and_text.utils.transformer_whisper import load_model

# API Doc
if os.getenv("ENVIRONMENT") == "local":
    spell_and_text_app = FastAPI(
        title="SpellAndTextApp",
        description="Spell And Text Application",
        version="1.0.0",
        openapi_url="/api/v1/openapi.json",
        docs_url="/api/v1/docs",
        redoc_url="/api/v1/redoc",
        # root_path="/api/v1"
    )
else:
    spell_and_text_app = FastAPI(
        title="SpellAndTextApp",
        description="Spell And TextApplication",
        version="1.0.0",
        openapi_url="/api/v1/openapi.json",
        docs_url="/api/v1/docs",
        redoc_url="/api/v1/redoc",
        debug=True
        # root_path="/api/v1"
    )
spell_and_text_app.add_middleware(GZipMiddleware)
spell_and_text_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
spell_and_text_app.include_router(api_router, prefix='/api/v1')



@spell_and_text_app.on_event("startup")
async def start_database() -> None:
    logger = get_logger()
    logger.info("Initiating database........")
    # await initiate_database()
    logger.info("Initiating database completed........")
    # with open('openapi/spell_and_text/openapi.json', 'w') as f:
    #     json.dump(get_openapi(
    #         title=spell_and_text_app.title,
    #         version=spell_and_text_app.version,
    #         openapi_version=spell_and_text_app.openapi_version,
    #         description=spell_and_text_app.description,
    #         routes=spell_and_text_app.routes,
    #     ), f)

    logger.info("OpenAPI specification created.........")
    logger.info("Connecting to redis.........")
    # spell_and_text_app.state.redis_connection = await initiate_redis_pool()
    logger.info("Redis Connected.........")
    load_model("ml_model/whisper_small_bn")
    print("Model Loaded")


# @app.on_event("shutdown")
# async def shutdown_event():
#     logger.info("Closing Redis...")
#     await app.state.redis_connection.close()

#
PORT = 8000
BIND = '127.0.0.1'
WORKERS = 10
RELOAD = True
# app = FastAPI(
#     title="SkillMatrix",
#     description="Skill Matrix Application",
#     version="1.0.0")
# # app.mount("/auth", auth_management)
if __name__ == "__main__":
    # install_packages()
    # uvicorn.run("hello:app", host=BIND, port=int(PORT), reload=RELOAD, debug=RELOAD, workers=int(WORKERS))
    uvicorn.run("spell_and_text.main:spell_and_text_app", host=BIND, port=int(PORT), reload=RELOAD, workers=int(WORKERS))
