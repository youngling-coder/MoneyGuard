import os
from typing import Optional

from ..settings import application_settings


def get_profile_picture_if_exists(id: int) -> Optional[str]:
    profile_picture_filename = f"{application_settings.profile_picture_base_name}_{id}{application_settings.profile_picture_extension}"

    print(profile_picture_filename)

    profile_picture_path = os.path.join(application_settings.profile_picture_path, profile_picture_filename)

    print(profile_picture_path)

    if os.path.exists(profile_picture_path):
        return profile_picture_path