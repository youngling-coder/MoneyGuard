from fastapi import FastAPI
from .routers import auth, user, account


app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(account.router)