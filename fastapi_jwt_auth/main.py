"""
    The main module housing the FastAPI app.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.auth_routes import auth_router
from routes.main_routes import main_router


app = FastAPI(
    debug=True,
    title="FastAPI JWT Auth",
    description=("An example of using authenticating FastAPI using Javascript Web "
                "Tokens."),
    version="0.1.4",
    redoc_url=None
)


allowed_origins = [
    "http://localhost:8000",
    "https://fastapi-jwt-auth.deta.dev",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root() -> dict:
    return {"message": "Hello World"}


app.include_router(auth_router)
app.include_router(main_router)
