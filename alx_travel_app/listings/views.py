import uuid
from environ import Env
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from .models import Payment
from django.views import View
from .models import Booking
from .serializers import BookingSerializer
import requests
from listings.tasks import send_listing_email

env=Env()
env.read_env()

@method_decorator(csrf_exempt, name='dispatch')  # To ensure all HTTP methods skip CSRF checks
class InitiatePaymentView(View):
    def post(self, request, *args, **kwargs):
        # Get booking details from the request
        import json
        data = json.loads(request.body)

        email = data.get('email')
        amount = data.get('amount')
        full_name = data.get('amount')
        booking_id = data.get('booking_id')

        # link to an existing Booking object
        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return JsonResponse({"error": "Booking not found"}, status=404)

        if not all([email, amount, full_name, booking_id]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        # Prepare data for Chapa API
        CHAPA_SECRET_KEY=env('CHAPA_SECRET_KEY')
        CHAPA_API_URL = "https://api.chapa.co/v1/transaction/initialize"
        txt_ref= str(uuid.uuid4())  # generating a unique transaction reference for the payment request

        chapa_payload = {
            "amount": amount,
            "currency": "ETB",
            "email":email,
            "first_name":full_name.split()[0],
            "last_name": full_name.split()[-1] if len(full_name.split()) > 1 else "",
            "txt_ref": txt_ref,
            "callback_url": "https://8804-41-90-172-227.ngrok-free.app/chapa/callback/",  # optional
            "return_url": "https://yourdomain.com/payment-success/",
            "customization": {
                "title": "Booking Payment",
                "description": "Payment for travel booking"
            }
        }

        headers = {
            "Authorization": f"Bearer {CHAPA_SECRET_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(CHAPA_API_URL, json=chapa_payload, headers=headers)  # Sends a payment initiation request to Chapa
        chapa_response= response.json()
        print(chapa_response)
        if chapa_response.get('status') == 'success':
            # Save payment
            Payment.objects.create(
                booking_id= booking,
                email= email,
                full_name= full_name,
                amount= amount,
                transaction_id=txt_ref,
                payment_status= 'Pending'
            )

            return JsonResponse({
                "Message": "Payment initiated successfully",
                "checkout_url": chapa_response['data']['checkout_url'],
                "txt_ref": txt_ref,
                "status": " PENDING"
            })
        else:
            return JsonResponse({'error': 'Chapa payment initiation failed'}, status=500)
        
@csrf_exempt
def verify_payment(request, tx_ref):

    CHAPA_SECRET_KEY=env('CHAPA_SECRET_KEY')
    url = f"https://api.chapa.co/v1/transaction/verify/{tx_ref}"
    headers = {
        'Authorization': f"Bearer {CHAPA_SECRET_KEY}"
    }

    #  Make a GET request to Chapa's Verify API
    response = requests.get(url, headers=headers)
    results = response.json()
    print(results)

    try:
        payment = Payment.objects.get(transaction_id=tx_ref)
    except Payment.DoesNotExist:
        return JsonResponse({'error':'Payment record not found in your database.'}, status=404)
    
    # Process Chapa's verification response
    if results.get('status') == "success" and results['data']['status'] == "success":
        # payment was successful!
        payment.status = 'SUCCESS'
        payment.save()
        return JsonResponse({'Message': 'Payment verified successfully'})
    else:
        # Verification failed!
        payment.status = 'FAILED'
        payment.save()
        return JsonResponse({'Message': 'Payment verification failed'}, status=404)



class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()

        # Trigger Celery emailtask
        send_listing_email.delay(booking.listing.id)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)