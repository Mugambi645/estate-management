

from pathlib import Path
from os import getenv, path


from dotenv import load_dotenv

from .base import * #noqa

from .base import BASE_DIR

for env_file in (path.join(BASE_DIR, ".envs", ".env.local"), path.join(BASE_DIR, ".envs", ".env.production")):
    if path.isfile(env_file):
        load_dotenv(env_file)


DEBUG = True

SITE_NAME = getenv("SITE_NAME", "Pegasus Apartments")



SECRET_KEY = getenv("DJANGO_SECRET_KEY",
                    "hSEK1qArROHXyOPfe8tsvDNql_RXEKVtCIO8cPW0kLsrvYHyGIs")



ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]


ADMIN_URL = getenv("DJANGO_ADMIN_URL", "")
DEFAULT_FROM_EMAIL = getenv("DEFAULT_FROM_EMAIL", "patrick@localhost")
DOMAIN = getenv("DOMAIN", "localhost")



LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(name)-12s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"],
    },
}