from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from lol_chatter_backend import auth
from lol_chatter_backend.DbInitialization.db import Base, engine
from lol_chatter_backend.routes import chatting
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
    # Add more allowed origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(chatting.router, prefix="/chatting", tags=["chatting"])
