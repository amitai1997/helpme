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

router = routers.DefaultRouter()
router.register(r"emergency-calls", EmergencyCallViewSet)
router.register(r"volunteers", VolunteerViewSet)
router.register(r"rescue-teams", RescueTeamViewSet)  # optional
router.register(r"notifications", NotificationViewSet)
router.register(r"user-locations", UserLocationViewSet)
router.register(r"profiles", ProfileViewSet)
router.register(r"emergency-type", EmergencyTypeViewSet)

urlpatterns = [
    path("volunteers/map/", CustomAdminView, name="volunteers_map"),
    path("volunteers/update/", UpdateVolunteersView, name="updated_volunteers"),
    path("view_volunteer_location/<int:volunteer_id>/", view_volunteer_location, name="view_volunteer_location"),
    path("ratings/", include("star_ratings.urls", namespace="ratings")),
    # URL for rating a volunteer
    path("volunteer/<int:volunteer_id>/rate/", rate_volunteer, name="rate_volunteer"),
    path("volunteer/<int:volunteer_id>/info/", volunteer_rating_info, name="volunteer_detail"),
    path("", include(router.urls)),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
