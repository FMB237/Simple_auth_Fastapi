# This is mainly a simple Auth System i will be build step by steps using Chatgpt Alongside of me

App Structure : 
app/
 ├── main.py
 ├── templates/
 │    ├── base.html
 │    ├── login.html
 │    ├── register.html
 │    └── dashboard.html
 ├── static/
 │    └── css/
 └── db/
     └── users.db

**1.Install depencies** 
The will be find inside the requirement.txt file 


Let add a real db and models.py for this work 

Let move on to step 8 Setting up Security and Session
So we will add : 
- Password hashing
- Session(Login stay in )
- Redirect in dashboard
Let install the necessary packets for that 
Using the command **pip install passlib[bcrypt] itsdangerous**
1. Let add password hash which is generally added into a file called auth.py for here we will just import it to our main.py file
2. 