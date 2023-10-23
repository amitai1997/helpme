from django.apps import AppConfig


def create_emergency_types(sender, **kwargs):
    EmergencyType = sender.get_model("EmergencyType")
    for choice in EmergencyType.EMERGENCY_CHOICES:
        EmergencyType.objects.get_or_create(name=choice[0])


class EmergencyConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "helpme.emergency"

    def ready(self):
        # post_migrate.connect(create_emergency_types, sender=self)
        import helpme.emergency.signals as signals

        print(signals)
