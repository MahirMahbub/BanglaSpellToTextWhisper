from fastapi import APIRouter

from spell_and_text.controllers import test

api_router: APIRouter = APIRouter()
api_router.include_router(test.test_router)
