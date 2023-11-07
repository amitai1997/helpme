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
from helpme.emergency.views import (
    CustomAdminView,
    UpdateVolunteersView,
    rate_volunteer,
    view_volunteer_location,
    volunteer_rating_info,
)

app_name = "emergency"

# Define the API router
router = routers.DefaultRouter()
router.register(r"emergency-calls", EmergencyCallViewSet)
router.register(r"volunteers", VolunteerViewSet)
router.register(r"rescue-teams", RescueTeamViewSet)  # Optional
router.register(r"notifications", NotificationViewSet)
router.register(r"user-locations", UserLocationViewSet)
router.register(r"profiles", ProfileViewSet)
router.register(r"emergency-types", EmergencyTypeViewSet)

# Define the URL patterns
urlpatterns = [
    # Regular views
    path("volunteers/map/", CustomAdminView, name="volunteers_map"),
    path("volunteers/update/", UpdateVolunteersView, name="update_volunteers"),
    path("volunteers/<int:volunteer_id>/location/", view_volunteer_location, name="volunteer_location"),
    # Ratings and API views
    path("api/volunteers/<int:volunteer_id>/rate/", rate_volunteer, name="rate_volunteer"),
    path("api/volunteers/<int:volunteer_id>/info/", volunteer_rating_info, name="volunteer_info"),
    # Include API routes
    path("api/", include(router.urls)),
]
