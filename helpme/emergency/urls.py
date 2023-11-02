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
from helpme.emergency.views import CustomAdminView, SendEmailView, UpdateVolunteersView, view_volunteer_location

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
    path("send-email/", SendEmailView.as_view(), name="send_email"),
    path("volunteers/map/", CustomAdminView, name="volunteers_map"),
    path("volunteers/update/", UpdateVolunteersView, name="updated_volunteers"),
    path("view_volunteer_location/<int:volunteer_id>/", view_volunteer_location, name="view_volunteer_location"),
    path("", include(router.urls)),
]
