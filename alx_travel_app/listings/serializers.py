from rest_framework import serializers
from .models import Listing, Booking, Review, Payment

class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = [ 'title', 'description', 'location', 'price_per_night', 'available', 'created_at']
        
    class Meta:
        model = Booking
        fields = '__all__'

    class Meta:
        model = Payment
        fields = '__all__'