from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class IssuesConfig(AppConfig):
    name = "core_apps.issues"
    verbose_name = _("Issues")