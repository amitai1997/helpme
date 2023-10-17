from django.urls import include, path
from rest_framework import routers

from helpme.emergency.api.views import (
    EmergencyCallViewSet,
    NotificationViewSet,
    ProfileViewSet,
    RescueTeamViewSet,
    UserLocationViewSet,
    VolunteerViewSet,
)

app_name = "emergency"

router = routers.DefaultRouter()
router.register(r"emergency-calls", EmergencyCallViewSet)
router.register(r"volunteers", VolunteerViewSet)
router.register(r"rescue-teams", RescueTeamViewSet)  # optional
router.register(r"notifications", NotificationViewSet)
router.register(r"user-locations", UserLocationViewSet)
router.register(r"profiles", ProfileViewSet)

urlpatterns = [
    # ... your other URL patterns ...
    path("", include(router.urls)),
]
