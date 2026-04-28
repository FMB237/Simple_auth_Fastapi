from fastapi import FastAPI,Request,HTTPException,Depends,status,Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.staticfiles import StaticFiles
from models import User
from database import Base,engine,SessionLocal
from passlib.context import  CryptContext
from starlette.middleware.sessions import SessionMiddleware
import uvicorn


app= FastAPI()

templates= Jinja2Templates(directory='./templates')

# Let mount our css
app.mount("/app/static",StaticFiles(directory="./static"),name="static")

Base.metadata.create_all(bind=engine)

# The middleware in quetion

app.add_middleware(
    SessionMiddleware,
    secret_key="941f8c9cf212dbecdc17792b8db8c2246f988cd0a38b9f6ac8d0097be2eb3bf2"
)


# Let add some security to our code
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")



# Now add the helpfull auth functions

def hash_password(password:str):
    return pwd_context.hash(password[:72])

def verify_password(plain,hashed):
    return pwd_context.verify(plain,hashed)

# Let add a session using middlewares


@app.get('/',response_class=HTMLResponse)
def home(request : Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )
# Let now add a post request for our Form
# Also update the login 
@app.post('/login',response_class=HTMLResponse)
def login(request:Request,username : str = Form(...) , password: str = Form(...)):
    db= SessionLocal()
    try:
         user = db.query(User).filter(User.username == username).first()
         if user and verify_password(password,user.password):
           request.session["user"] = user.username
           return HTMLResponse(
            '<script>window.location.href="/dashboard"</script>')
             # fOR Redirection to dashboard after login
         else:
            return "<p style='color:red;'>Invalid credentials</p>"
    finally:
        db.close()

   


#Let add the SignUp route for get request
@app.get("/SignUp",response_class=HTMLResponse)
def get_SignUp(request:Request):
    return templates.TemplateResponse(
     request=request,
     name="SignUp.html"
    )

# Let add our Signup route for post requests
# Update SignUp with new password rules
@app.post('/SignUp',response_class=HTMLResponse)
def Post_SignUp(request:Request,username : str = Form(...),email:str = Form(...),password: str = Form(...,)):
    db =SessionLocal()
    try:
        existing_user = db.query(User).filter(User.username == username).first()  # Now let check if user exists ??
        if existing_user:
             return "<p style='color:red;'>User already exists</p>"

         # new password variable
        hashed_pw = hash_password(password)
        new_user = User(username=username,email=email,password=hashed_pw)
        db.add(new_user)
        db.commit()
        return "<p style='color:green;'>Registration successful</p>"
    finally:
        db.close()
    


# let add our dashboard route
@app.get("/dashboard",response_class=HTMLResponse)
def get_dashboard(request:Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/")
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html"
    )    


# Let add logout
@app.get("/logout")
def logout(request:Request):
    request.session.clear()
    return RedirectResponse(url="/")
if __name__=="__main__":
    uvicorn.run('main:app',host="0.0.0.0",port=8001,reload=True)
