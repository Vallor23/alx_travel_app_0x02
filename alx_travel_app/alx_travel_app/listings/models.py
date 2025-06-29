from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.
class Listing(models.Model):
        title = models.CharField(max_length=50)
        description = models.CharField(max_length=255)
        location = models.CharField(max_length=50)
        price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
        available = models.BooleanField()
        created_at = models.DateTimeField(auto_now_add=True)
         
        class Meta:
                ordering = ['-created_at']
                
        def __str__(self):
                return self.title
class Booking(models.Model):
        total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
        start_date = models.DateField()
        end_date = models.DateField()        
        listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bookings')
        
        # Ensure end_date is not before start_date
        def clean(self):
                if self.start_date and self.end_date:
                        if self.end_date < self.start_date:
                              raise ValidationError({
                                       'end_date': 'End date cannot be before start date.'
                              })

        def save(self, *args, **kwargs):
               nights = (self.end_date- self.start_date ).days
               self.total_cost = nights * self.listing.price_per_night
               self.full_clean()
               super().save(*args, **kwargs)

        def __str__(self):
                return f"Booking for {self.listing} from {self.start_date} to {self.end_date}"
class Review(models.Model):
        reviewer_name = models.CharField(max_length=50)
        rating = models.PositiveIntegerField(choices=[(i,i) for i in range(1,6)])
        comment = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True)
        listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reviews')

        class Meta:
                 ordering = ['-created_at', '-rating'] # Order by creation, then by rating

        def __str__(self):
                return f"{self.reviewer_name} for {self.listing.title}  - {self.rating}"