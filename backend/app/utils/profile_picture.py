import os

from ..settings import application_settings


def get_profile_picture_url(id: int) -> str:
    profile_picture_filename = f".{application_settings.profile_picture_path}/{application_settings.profile_picture_filename}{id}{application_settings.profile_picture_extension}"

    profile_picture_url = os.path.join(
        application_settings.profile_picture_path, profile_picture_filename
    )
    profile_picture_url = os.path.abspath(profile_picture_filename)

    return profile_picture_url
