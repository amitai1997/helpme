from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from leaflet.admin import LeafletGeoAdmin

from helpme.emergency.models import Profile, Volunteer


@admin.register(Volunteer)
class VolunteerAdmin(LeafletGeoAdmin):
    list_display = (
        "get_profile_user_link",
        "profile",
        "location",
        "availability_status",
        "contact_information",
        "preferred_area",
        "carrying_weapon",
        "driving_license",
        "view_location_link",  # Include the custom method here
    )
    map_height = "500px"
    map_width = "100%"
    list_max_show_all = 5000

    @admin.display(description="Location Link")
    def view_location_link(self, obj):
        if obj.profile.user:
            url = reverse(
                "emergency:view_volunteer_location", args=[obj.id]
            )  # Adjust the URL pattern as per your project
            return format_html('<a href="{}" target="_blank">View Location</a>', url)
        return "N/A"  # Or any message you want to display if the user is not available

    @admin.display(ordering="profile__user", description="User")
    def get_profile_user(self, obj):
        return obj.profile.user.email

    @admin.display(ordering="profile__user", description="User")
    def get_profile_user_link(self, obj):
        if obj.profile.user:
            app_label = obj.profile._meta.app_label  # Get the app label
            model_name = obj.profile._meta.model_name  # Get the model name
            url = reverse(f"admin:{app_label}_{model_name}_change", args=[obj.profile.user.id])
            return format_html('<a href="{}">{}</a>', url, obj.profile.user.email)
        return "N/A"  # Or any message you want to display if the user is not available


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("get_profile_user", "identification_number", "gender", "date_of_birth", "address")

    @admin.display(ordering="profile__user", description="User")
    def get_profile_user(self, obj):
        return obj.user.email
