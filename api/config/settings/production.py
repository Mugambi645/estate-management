
from os import getenv, path


from dotenv import load_dotenv

from .base import * #noqa

from .base import BASE_DIR

for env_file in (path.join(BASE_DIR, ".envs", ".env.local"), path.join(BASE_DIR, ".envs", ".env.production")):
    if path.isfile(env_file):
        load_dotenv(env_file)



SECRET_KEY = getenv("DJANGO_SECRET_KEY", "change-me-in-production")



ALLOWED_HOSTS = ["*"]


ADMINS = [("Patrick Mugambi", "mugambi645@gmail.com"),]