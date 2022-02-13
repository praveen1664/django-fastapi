from tkinter import Image
from django.http import response
from fastapi.testclient import TestClient
# from isort import file
from app.main import app, BASE_DIR, UPLOADED_DIR
import shutil
import time
from PIL import Image, ImageChops
import io


client=TestClient(app)

def test_get_home():
    response=client.get("/") #request to hom,e
    assert response.status_code == 200
    assert 'text/html' in response.headers['content-type']


def test_home_detail_view():
    response=client.post("/")
    assert response.status_code==200
    assert "application/json" in response.headers['content-type']
    assert response.json() == {"Hello":"Praveen Singh"}

valid_image_extension=['png','jpeg','jpg','jfif']
def testEchoUpload():
    img_saved_path=BASE_DIR / "Images"
    # path=list(().glob("*"))[0]
    for path in img_saved_path.glob("*"):
        response=client.post("/img-echo/",files={"file":open(path,'rb')})
        # fext=str(path.suffix).replace('.','')
        # fext=fext.replace('jfif','jpeg')
        # if fext in valid_image_extension:
        try:
            img=Image.open(path)
        except:
            img=None
        if img is None:
            # assert fext in response.headers['content-type']
            assert response.status_code==400
        else:
            #returning a valid image
            assert response.status_code==200
            r_stream=io.BytesIO(response.content)
            echo_img=Image.open(r_stream)
            difference=ImageChops.difference(echo_img,img).getbbox()
            # assert difference is None

        # print(f"Path is \n {path} \n ******")

        # fext=fext.replace('jfif','jpeg')

        # assert "application/json" in response.headers['content-type']
        # assert response.json() == {"Hello":"Praveen Singh"}
        # print("*********Desired heaers are*********")
        # print(response.headers)
        # print(path.suffix)
        # fext=str(path.suffix).replace('jfif','jpeg')

        # print(fext)
    # time.sleep(3)
    shutil.rmtree(UPLOADED_DIR)

