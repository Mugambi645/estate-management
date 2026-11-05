"""Custom user model for the estate_prod API.

Email is the login identifier; a UUID ``id`` is exposed publicly while the
internal ``pkid`` BigAutoField is the primary key used for joins.
"""

import uuid

from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _

from core_apps.users.managers import UserManager


class UsernameValidator(validators.RegexValidator):
    """Allow letters, digits, and ``.@+-`` in usernames."""

    regex = r"^[\w.@+-]+\Z"
    message = _(
        "Your username is not valid. A username can only contain letters, "
        "numbers, a dot, @ symbol, + symbol and a hyphen."
    )
    flag = 0


class User(AbstractUser):
    """Project user model.

    * ``pkid`` — internal BigAutoField primary key.
    * ``id``   — public, unguessable UUID exposed via the API.
    * ``email`` — login identifier (``USERNAME_FIELD``).
    * ``username`` — still required and unique, but not used to log in.
    """

    pkid = models.BigAutoField(primary_key=True, editable=False)

    id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True,
    )

    first_name = models.CharField(
        verbose_name=_("First Name"),
        max_length=60,
    )
    last_name = models.CharField(
        verbose_name=_("Last Name"),
        max_length=60,
    )
    email = models.EmailField(
        verbose_name=_("Email Address"),
        unique=True,
        db_index=True,
    )
    username = models.CharField(
        verbose_name=_("Username"),
        max_length=60,
        unique=True,
        validators=[UsernameValidator()],
    )

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    objects = UserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ["-date_joined"]

    def get_full_name(self) -> str:
        """Return the user's first and last name, space-separated."""
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    def __str__(self) -> str:
        """String representation used in admin and logs."""
        return self.email