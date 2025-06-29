from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListingViewSet, BookingViewSet, ReviewViewSet


router = DefaultRouter()
router.register(r'listing', ListingViewSet, basename='listing')
router.register(r'booking', BookingViewSet, basename='bookings')
router.register(r'review', ReviewViewSet, basename='reviews')


urlpatterns = [
    path('api/', include(router.urls)),
]