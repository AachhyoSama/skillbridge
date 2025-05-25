from fastapi import FastAPI
from routes import users, auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow requests from your frontend (Vite typically uses 5173)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",  # Optional if you access via 127.0.0.1
]

# Add the CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Origins that are allowed
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers (Authorization, Content-Type, etc.)
)

app.include_router(users.router)
app.include_router(auth.router)
