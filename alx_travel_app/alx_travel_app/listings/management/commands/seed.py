from django.core.management.base import BaseCommand
from django.apps import apps
from ...models import Listing
class Command(BaseCommand):
    help = 'Populates the database with sample listing data.'
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting database seeding...'))

        # clear existing listings
        Listing.objects.all().delete()
        
       # Define your sample listings data
        sample_listings = [
            {
                'title': 'Cozy Apartment in Nairobi',
                'description': 'A charming and comfortable apartment near the city center, perfect for solo travelers or couples.',
                'location': 'Nairobi, Kenya',
                'price_per_night': 50.00,
                'available': True,
            },
            {
                'title': 'Luxury Villa with Ocean View',
                'description': 'Stunning villa located on the coast, offering breathtaking ocean views and a private pool.',
                'location': 'Mombasa, Kenya',
                'price_per_night': 250.00,
                'available': True,
            },
            {
                'title': 'Rustic Safari Tent',
                'description': 'Experience the wilderness in comfort with this unique safari tent, close to wildlife parks.',
                'location': 'Maasai Mara, Kenya',
                'price_per_night': 120.00,
                'available': False,
            },
            {
                'title': 'Downtown Studio Loft',
                'description': 'Modern studio in the heart of the business district, ideal for short-term business trips.',
                'location': 'Nairobi, Kenya',
                'price_per_night': 75.00,
                'available': True,
            },
        ]
        
        for data in sample_listings:
            Listing.objects.create(**data)
            self.stdout.write(self.style.SUCCESS(f"Added listing: {Listing.title}"))
            
        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully!'))