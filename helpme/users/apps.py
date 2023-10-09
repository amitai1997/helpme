from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "helpme.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import helpme.users.signals  # noqa: F401
        except ImportError:
            pass
