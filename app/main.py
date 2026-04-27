from fastapi import FastAPI,Request,HTTPException,Depends,status,Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from models import User
from database import Base,engine,SessionLocal
import uvicorn


app= FastAPI()

templates= Jinja2Templates(directory='./templates')

Base.metadata.create_all(bind=engine)


@app.get('/',response_class=HTMLResponse)
def home(request : Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )
# Let now add a post request for our Form

@app.post('/login',response_class=HTMLResponse)
def login(request:Request,username : str = Form(...) , password: str = Form(...)):
    db= SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    if user and user.password == password:
         return "<p style='color:green;'>Login successful</p>"
         
    return "<p style='color:red;'>Invalid credentials</p>"


#Let add the SignUp route for get request
@app.get("/SignUp",response_class=HTMLResponse)
def get_SignUp(request:Request):
    return templates.TemplateResponse(
     request=request,
     name="SignUp.html"
    )

# Let add our Signup route for post requests
@app.post('/SignUp',response_class=HTMLResponse)
def SignUp(request:Request,username : str = Form(...),email:str = Form(...),password: str = Form(...,)):
    db =SessionLocal() # Now let check if user exists ??
    existing_user = db.query(User).filter(User.username == username).first()

    if existing_user:
         return "<p style='color:red;'>User already exists</p>"
    new_user = User(username=username,email=email,password=password)
    db.add(new_user)
    db.commit()
    return "<p style='color:green;'>Registration successful</p>"

if __name__=="__main__":
    uvicorn.run('main:app',host="0.0.0.0",port=8001,reload=True)
