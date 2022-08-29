# from deta import Deta
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.auth_routes import auth_router
from routes.main_routes import main_router


# deta = Deta()
# users_db = deta.Base("users")

app = FastAPI(
    debug=True,
    title="FastAPI JWT Auth",
    description=("An example of authenticating FastAPI using Javascript Web "
                "Tokens."),
    version="0.1.3",
    redoc_url=None
)

# allowed_origins = [
#     "http://localhost",
#     "http://localhost:8080",
#     "http://localhost:3000",
#     "https://fastapi-fast-auth.deta.dev/",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=allowed_origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


@app.get("/")
async def root() -> dict:
    return {"message": "Hello World"}


app.include_router(auth_router)
app.include_router(main_router)
