import os, json, requests, uuid
from django.http import JsonResponse
from django.views import View
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Donation

PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY", "sk_test_xxx")  # from .env

@method_decorator(csrf_exempt, name="dispatch")
class InitializePaymentView(View):
    def post(self, request):
        data = json.loads(request.body)

        amount = int(float(data.get("amount")) * 100)  # convert to kobo
        email = data.get("donor_email")
        name = data.get("donor_name")
        reference = str(uuid.uuid4())

        headers = {"Authorization": f"Bearer {PAYSTACK_SECRET_KEY}"}
        payload = {
            "email": email,
            "amount": amount,
            "reference": reference,
            "callback_url": "http://localhost:5173/payment-success",
        }

        response = requests.post(
            "https://api.paystack.co/transaction/initialize",
            headers=headers,
            json=payload
        ).json()

        if response.get("status"):
            # Save donation as pending
            Donation.objects.create(
                uuid=reference,
                donor_name=name,
                donor_email=email,
                amount=data.get("amount"),
                status="pending",
            )
            return JsonResponse({"checkout_url": response["data"]["authorization_url"]})

        return JsonResponse({"error": response.get("message")}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class VerifyPaymentView(View):
    def get(self, request, reference):
        headers = {"Authorization": f"Bearer {PAYSTACK_SECRET_KEY}"}
        response = requests.get(
            f"https://api.paystack.co/transaction/verify/{reference}",
            headers=headers
        ).json()

        try:
            donation = Donation.objects.get(uuid=reference)
        except Donation.DoesNotExist:
            return JsonResponse({"status": "failed", "error": "Donation not found"}, status=404)

        if response.get("status") and response["data"]["status"] == "success":
            donation.payment_method = "Paystack"
            donation.transaction_id = response["data"]["id"]
            donation.status = "success"
            donation.save()
            return JsonResponse({"status": "success", "data": response["data"]})

        # If payment failed
        donation.status = "failed"
        donation.save()
        return JsonResponse({"status": "failed", "error": response.get("message")}, status=400)
