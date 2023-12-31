from django.urls import include, path
from rest_framework import routers

from helpme.emergency.api.views import (
    EmergencyCallViewSet,
    EmergencyTypeViewSet,
    NotificationViewSet,
    ProfileViewSet,
    RescueTeamViewSet,
    UserLocationViewSet,
    VolunteerViewSet,
)
from helpme.emergency.views import SendEmailView

app_name = "emergency"

router = routers.DefaultRouter()
router.register(r"emergency-calls", EmergencyCallViewSet)
router.register(r"volunteers", VolunteerViewSet)
router.register(r"rescue-teams", RescueTeamViewSet)  # optional
router.register(r"notifications", NotificationViewSet)
router.register(r"user-locations", UserLocationViewSet)
router.register(r"profiles", ProfileViewSet)
router.register(r"emergency-type", EmergencyTypeViewSet)

urlpatterns = [
    # ... your other URL patterns ...
    path("send-email/", SendEmailView.as_view(), name="send_email"),
    path("", include(router.urls)),
]
