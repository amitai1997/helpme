import json

# from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import AnonymousUser
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.forms import ValidationError
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from star_ratings.models import Rating, UserRating

from helpme.emergency.api.serializers import VolunteerSerializer
from helpme.emergency.models import Volunteer


# @staff_member_required
@csrf_exempt
def UpdateVolunteersView(request):
    # Fetch all EmergencyCall objects and select related ratings
    volunteers = Volunteer.objects.select_related("rating").all()

    # Serialize the queryset using the serializer
    serializer = VolunteerSerializer(volunteers, many=True)

    return JsonResponse({"volunteers": json.dumps(serializer.data)}, safe=False)
    # return HttpResponse(json.dumps({"volunteers": serializer.data}), content_type="application/json")


# @staff_member_required
@csrf_exempt
def CustomAdminView(request):
    # Fetch all EmergencyCall objects
    volunteers = Volunteer.objects.all()

    for volunteer in volunteers:
        # Retrieve all ratings associated with the volunteer
        ratings = Rating.objects.filter(
            object_id=volunteer.id,
        )
        volunteer.average_rating = ratings.aggregate(average_rating=models.Avg("average"))["average_rating"] or 0

    return render(
        request,
        # TODO change to relative location
        "admin/display_all_volunteers.html",
        {"volunteers": volunteers},
    )


def view_volunteer_location(request, volunteer_id):
    volunteer = Volunteer.objects.get(pk=volunteer_id)

    # Add code to handle displaying the location on the map
    # You can pass the volunteer's location data to your template
    return render(request, "admin/volunteer_location.html", {"volunteer": volunteer})


@csrf_exempt
def rate_volunteer(request, volunteer_id):
    if request.method == "POST":
        try:
            rating_value = json.loads(request.body).get("rating")

            # Validate rating value
            rating_value = json.loads(request.body).get("rating")
            if not (0 <= rating_value <= 5):  # Assuming a rating scale from 0 to 5
                raise ValidationError("Invalid rating value")

            volunteer = Volunteer.objects.get(id=volunteer_id)
            user = request.user

            # Check if the user is anonymous
            if isinstance(user, AnonymousUser):
                # Handle anonymous user rating

                # Create a placeholder user for anonymous ratings (if not exists)
                # placeholder_user, created = User.objects.get_or_create(username="Anonymous User")
                # user = placeholder_user
                user = None

            content_type = ContentType.objects.get_for_model(volunteer)

            # Create a new Rating instance or get an existing one
            rating, created = Rating.objects.get_or_create(
                content_type=content_type,
                object_id=volunteer.id,
            )

            # Set the rating value
            rating.rating = rating_value
            rating.save()

            # Set the volunteer's rating to the newly created or updated rating
            volunteer.rating = rating
            volunteer.save()

            # Calculate the score for the UserRating based on the Rating
            user_rating = UserRating(
                score=rating_value,
                rating=rating,
                user=user,
            )
            user_rating.save()

            # Recalculate the totals, and save.
            rating.calculate()

            # Return a JSON response indicating success
            return JsonResponse({"message": "Rating added successfully"})

        except ObjectDoesNotExist:
            return JsonResponse({"error": "Volunteer not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # Handle other HTTP methods (e.g., GET) if needed
    return JsonResponse({"error": "Invalid request method"}, status=405)


def volunteer_rating_info(request, volunteer_id):
    if request.method == "GET":
        try:
            volunteer_id = int(volunteer_id)  # Convert to integer
            volunteer = Volunteer.objects.get(id=volunteer_id)

            # Retrieve all ratings associated with the volunteer
            ratings = Rating.objects.filter(
                object_id=volunteer.id,
            )

            average_rating = ratings.aggregate(average_rating=models.Avg("average"))["average_rating"] or 0
            total_ratings = ratings.aggregate(average_rating=models.Avg("count"))["average_rating"] or 0

            response_data = {
                "total_ratings": total_ratings,
                "average_rating": average_rating,
            }

            return JsonResponse(response_data)

        except ObjectDoesNotExist:
            return JsonResponse({"error": "Volunteer not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # Handle other HTTP methods (e.g., POST) if needed
    return JsonResponse({"error": "Invalid request method"}, status=405)
