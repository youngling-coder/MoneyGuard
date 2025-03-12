import os

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, status
from fastapi.staticfiles import StaticFiles

from .routers import auth, user, account, security_code_session, transaction
from .settings import application_settings

app = FastAPI()

origins = ["https://kristinapotapenko.github.io"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if not os.path.exists(application_settings.profile_pictures_path):
    try:
        os.mkdir(application_settings.profile_pictures_path)
    except FileExistsError:
        pass
    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error: Permission Denied",
        )
    except OSError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error: Unable to create directory",
        )

app.mount(
    application_settings.profile_pictures_mount_point,
    StaticFiles(directory=application_settings.profile_pictures_path),
    name="static",
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(account.router)
app.include_router(transaction.router)
app.include_router(security_code_session.router)
