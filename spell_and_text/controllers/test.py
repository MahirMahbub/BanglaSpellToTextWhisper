import os
import tempfile

import aiofiles
# import aiofiles as aiofiles
from fastapi import APIRouter, Depends, Request, UploadFile, HTTPException, status, File
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from spell_and_text.utils import transformer_whisper
from spell_and_text.utils.auth_manager import JWTBearer
from spell_and_text.utils.logger import get_logger
from fastapi import APIRouter, Depends, Request

from spell_and_text.utils.auth_manager import JWTBearer
from spell_and_text.utils.logger import get_logger

# from skill_management.models.plan import Plan

test_router: APIRouter = APIRouter()
logger = get_logger()
# templates = Jinja2Templates(directory="templates")
CHUNK_SIZE = 1024 * 1024


# @test_router.get("/hello/{name}")
# async def say_hello(request: Request, name: str, user_id: str = Depends(JWTBearer())):
#     # plan = Plan(skill_id=1)
#     # await plan.insert()
#     # logger.info("Testing Route")
#     # return {"message": f"Hello {name}", "plan": plan.id}
#     # redis = await aioredis.from_url(
#     #     os.getenv("REDIS_AUTH_URL"),
#     #     password=os.getenv("REDIS_PASSWORD"),
#     #     encoding="utf-8",
#     #     db=os.getenv("REDIS_USER_DB"),
#     #     decode_responses=True,
#     # )
#     # await request.app.state.redis_connection.set("my-key", "value")
#     val = await request.app.state.redis_connection.hgetall(user_id)
#     print(val)
#     return val

@test_router.post("/listen")
async def listen(request: Request, file: UploadFile = File(...)):
    try:
        temp_dir = tempfile.mkdtemp()
        filepath = os.path.join(temp_dir, os.path.basename(file.filename))
        async with aiofiles.open(filepath, 'wb') as f:
            while chunk := await file.read(CHUNK_SIZE):
                await f.write(chunk)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='There was an error uploading the file')
    finally:
        await file.close()
    model = transformer_whisper.load_model(r"G:\SpeechToText\bn_models\whisper_small_bn")

    result = model.transcribe(audio=filepath, language="bn",
                              task="transcribe", verbose=False)
    whisper_segments = result.get('segments')
    return whisper_segments

    # return {"message": f"Successfuly uploaded {file.filename}", "filepath": filepath}

    # save_path = os.path.join(temp_dir, 'temp.wav')

    # wav_file = request.files['audio_data']
    # wav_file.save(save_path)







@test_router.get("/", response_class=HTMLResponse)
def get(request: Request):
    return templates.TemplateResponse("test.html", {"request": request})
