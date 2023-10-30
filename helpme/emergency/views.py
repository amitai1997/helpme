from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import View

from helpme.emergency.models import EmergencyCall
from helpme.emergency.tasks import send_notification_email


class SendEmailView(View):
    def get(self, request):
        """Enqueue a task to send an email when the feedback form has been submitted."""
        message = request.GET.get("message", "")
        email_address = request.GET.get("email_address", "")

        if not email_address:
            return JsonResponse({"error": "email_address is required."}, status=400)

        try:
            result = send_notification_email.delay(email_address, message)
            return JsonResponse({"message": "Email will be sent in the background.", "task_id": result.id})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


#
@staff_member_required
def CustomAdminView(request):
    # Fetch all EmergencyCall objects
    emergency_calls = EmergencyCall.objects.all()
    return render(
        request,
        "admin/custom_emergencycall_view.html",
        {"emergency_calls": emergency_calls},
    )
