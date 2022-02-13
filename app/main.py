from distutils.debug import DEBUG
import json
import os
import pathlib
from PIL import Image
from fastapi import (
    FastAPI,
    Request,
    Depends,
    File,
    UploadFile,
    HTTPException)
import io
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseSettings
from functools import lru_cache
import uuid

# from streamlit import echo


# print(BASE_DIR)
# print((str(BASE_DIR/"templates")))
# Declaring the fast api app
# DEBUG=True if it is developement
# DEBUG=str(os.environ.get("DEBUG"))=="1" we want to be handle automatically

class Settings(BaseSettings):
    debug: bool=False
    echo_active: bool=False

    class Config:
        env_file=".env"


# settings=Settings()

@lru_cache
def getSettings():
    return Settings()

DEBUG=getSettings().debug
BASE_DIR=pathlib.Path(__file__).parent
UPLOADED_DIR=BASE_DIR / "uploads"
UPLOADED_DIR.mkdir(exist_ok=True)
print(BASE_DIR)
app=FastAPI()
template=Jinja2Templates(str(BASE_DIR/"templates"))

@app.get("/",response_class=HTMLResponse)
def home_view(request: Request,settings: Settings = Depends (getSettings)):
    return template.TemplateResponse("home.html",{"request":request})
    # print(request)
    # return "<h1>Hello Praveen</h1>"
    # return template.TemplateResponse("home.html",{"request":request})


@app.post("/")
def home_detail_view():
    return {"Hello":"Praveen Singh"}

@app.post("/img-echo/",response_class=FileResponse)
async def imageEchoView(file:UploadFile=File(...), settings: Settings=Depends(getSettings)):
    if not settings.echo_active:
        raise HTTPException (detail="Invalid EndPoint", status_code=400)
    byte_str=io.BytesIO(await file.read())
    try:
        img=Image.open(byte_str) # better uses Open cv
    except:
        raise HTTPException (detail="Invalid Image", status_code=400)

    fname=pathlib.Path(file.filename)
    fext=fname.suffix #
    dest= UPLOADED_DIR / f"{uuid.uuid1()}{fext}"
    # with open(str(dest),'wb') as out:
    #     out.write(byte_str.read())
    img.save(dest)
    return dest

