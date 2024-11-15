import os

from ..settings import application_settings


def get_profile_picture_url(id: int) -> str:
    profile_picture_filename = f"{application_settings.profile_picture_base_name}_{id}{application_settings.profile_picture_extension}"

    print(profile_picture_filename)

    profile_picture_url = os.path.join(application_settings.profile_picture_path, profile_picture_filename)

    print(profile_picture_url)

    return profile_picture_url
    