import json
import pathlib
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

BASE_DIR=pathlib.Path(__file__).parent
# print(BASE_DIR)
# print((str(BASE_DIR/"templates")))
# Declaring the fast api app
app=FastAPI()
template=Jinja2Templates(str(BASE_DIR/"templates"))
@app.get("/",response_class=HTMLResponse)
def home_view(request: Request):
    return template.TemplateResponse("home.html",{"request":request})
    # print(request)
    # return "<h1>Hello Praveen</h1>"
    # return template.TemplateResponse("home.html",{"request":request})


@app.post("/")
def home_detail_view():
    return {"Hello":"Praveen"}