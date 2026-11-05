"""Admin forms for the custom user model.

Because ``USERNAME_FIELD`` is ``email``, both forms are adjusted so the
unique-email and unique-username checks work correctly — Django's defaults
only validate ``USERNAME_FIELD`` uniqueness automatically.
"""

from django import forms
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm

User = get_user_model()


class UserChangeForm(BaseUserChangeForm):
    """Form used to edit an existing user in the admin."""

    class Meta(BaseUserChangeForm.Meta):
        model = User
        fields = ["first_name", "last_name", "username", "email"]


class UserCreationForm(admin_forms.UserCreationForm):
    """Form used to create a new user in the admin.

    Ensures both ``email`` and ``username`` are unique even though only
    ``USERNAME_FIELD`` (email) is validated by Django out of the box.
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = ["first_name", "last_name", "username", "email"]

    error_messages = {
        "duplicate_username": "A user with that username already exists.",
        "duplicate_email": "A user with that email already exists.",
    }

    def clean_email(self) -> str:
        """Reject duplicate emails (case-insensitive)."""
        email = self.cleaned_data["email"]
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(self.error_messages["duplicate_email"])
        return email

    def clean_username(self) -> str:
        """Reject duplicate usernames (case-insensitive)."""
        username = self.cleaned_data["username"]
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError(self.error_messages["duplicate_username"])
        return username