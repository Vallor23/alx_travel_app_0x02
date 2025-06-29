from rest_framework import serializers
from .models import Listing, Booking, Review

class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = [ 'title', 'description', 'location', 'price_per_night', 'available', 'created_at']
        
    class Meta:
        model = Booking
        fields = '__all__'