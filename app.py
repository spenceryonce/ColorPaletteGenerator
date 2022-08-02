from fastapi import FastAPI, Depends, Request, Form, status, Response
from fastapi.responses import HTMLResponse
from fastapi.responses import PlainTextResponse
from fastapi.responses import FileResponse
from pkg_resources import ResolutionError
#import dependencies for Image, ImageDraw
from PIL import Image, ImageDraw

from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from sqlalchemy.orm import Session

import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")


app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#setup the main route "/"
@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    colorpalettes = db.query(models.ColorPallete).all()
    context = {"request": request, "colorpalettes": colorpalettes,"title":"Tester"}
    return templates.TemplateResponse("base.html", context)

#setup the route "/add"
@app.post("/add")
def add(request: Request,name: str = Form(...),color1: str = Form(...),color2: str = Form(...),color3: str = Form(...),color4: str = Form(...),color5: str = Form(...), db: Session = Depends(get_db)):
    #create a new colorpallete
    colorpalette = models.ColorPallete(name=name,color1=color1,color2=color2,color3=color3,color4=color4,color5=color5)
    db.add(colorpalette)
    db.commit()

    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

#setup the route "/colorpalette/download/{id}"
@app.get("/colorpalette/download/{id}", response_class=FileResponse)
def download(id: int, db: Session = Depends(get_db)):
    colorpalette = db.query(models.ColorPallete).get(id)
    if not colorpalette:
        return {"message": "ColorPallete not found"}

    #create a new image 500px wide and 100px high
    img = Image.new("RGB", (500, 100), color=(255, 255, 255))
    #draw each color within colorpalette as a rectangle with a width of 100px each and a height of 100px each for the image
    img.paste(colorpalette.color1, (0, 0, 100, 100))
    img.paste(colorpalette.color2, (100, 0, 200, 100))
    img.paste(colorpalette.color3, (200, 0, 300, 100))
    img.paste(colorpalette.color4, (300, 0, 400, 100))
    img.paste(colorpalette.color5, (400, 0, 500, 100))

    #convert the img to a png in bytes
    img_bytes = img.convert("RGB").tobytes()

    #save the img to a file
    #img.save("colorpalette.png")
    img.save("colorpalette.png", "PNG")
    imgPath = "colorpalette.png"

    #return the img_bytes as a response
    return imgPath
    #return colorpalette as a formatted string in html with each color separated by a newline, ordering by color1, color2, color3, color4, color5
    #return f"{colorpalette.id}\n{colorpalette.name}\n{colorpalette.color1}\n{colorpalette.color2}\n{colorpalette.color3}\n{colorpalette.color4}\n{colorpalette.color5}"

#launch command = uvicorn api:api --reload



#setup the route /css/style.css
@app.get("/css/style.css")
def get_css(request: Request):
    return templates.TemplateResponse("css/style.css", {"request": request})

