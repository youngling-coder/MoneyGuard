import os
from typing import Annotated

from ..settings import application_settings


def __profile_picture_filename(id: int) -> str:
    return f"{application_settings.profile_picture_filename}{id}{application_settings.profile_picture_extension}"


def get_profile_picture_path(id: int) -> str:
    profile_picture_filename = f"{application_settings.profile_pictures_path}/{__profile_picture_filename(id=id)}"

    profile_picture_path = os.path.join(
        application_settings.profile_pictures_path, profile_picture_filename
    )
    profile_picture_path = os.path.abspath(profile_picture_filename)

    return profile_picture_path


def get_profile_picture_url(
    id: int, host: str = "https://cool-kite-divine.ngrok-free.app"
) -> str:

    profile_picture_url = f"{host}{application_settings.profile_pictures_mount_point}/{__profile_picture_filename(id=id)}"

    return profile_picture_url
