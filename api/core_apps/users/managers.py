"""Custom manager for the estate_prod ``User`` model.

The model uses **email as the login identifier** (``USERNAME_FIELD = "email"``),
so this manager's positional arguments are ordered to match Django's
expectations: ``email`` first, then ``password``.
"""

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _


def validate_email_address(email: str) -> None:
    """Validate ``email`` and raise a friendly ``ValidationError`` if invalid."""
    try:
        validate_email(email)
    except ValidationError:
        raise ValidationError(_("Enter a valid email address")) from None


class UserManager(DjangoUserManager):
    """Manager for the custom ``User`` model (email-based login)."""

    use_in_migrations = True

    def _create_user(
        self,
        email: str,
        password: str | None,
        **extra_fields,
    ):
        """Create and persist a user with a normalised, validated email."""
        if not email:
            raise ValueError(_("An email address must be provided"))

        email = self.normalize_email(email)
        validate_email_address(email)

        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self,
        email: str,
        password: str | None = None,
        **extra_fields,
    ):
        """Create a regular (non-staff, non-superuser) user."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(
        self,
        email: str,
        password: str | None = None,
        **extra_fields,
    ):
        """Create a superuser with ``is_staff=True`` and ``is_superuser=True``."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self._create_user(email, password, **extra_fields)