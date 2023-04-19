from fastapi import FastAPI
from .model import models
from .db import engine #, get_db
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware
# import psycopg2
# import psycopg2.extras
# import time
# from .schemas import schemas 
# from . import utils
# from sqlalchemy.orm import Session

# enviornment variable validation

# this line create tabel in db if table is not present if alembic is not used
# after alembic we dont required
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()
# database connection
# while True:
#     try:
#         conn = psycopg2.connect(
#             host="localhost", 
#             database='fastapi', 
#             user='postgres', 
#             password="admin", 
#             cursor_factory=psycopg2.extras.RealDictCursor
#         )
#         cursor = conn.cursor()
#         print("Database connection established!!!!")
#         break
#     except Exception as e:
#         print("Database connection error")
#         print(e)
#         time.sleep(2)


origins = [
    # "http://localhost",
    # "http://localhost:8080",
    # "https://www.google.com",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# routes

@app.get("/")
def root():
    return {"message": "Satyam"}

app.include_router(user.router)
app.include_router(post.router)
app.include_router(vote.router)
app.include_router(auth.router)