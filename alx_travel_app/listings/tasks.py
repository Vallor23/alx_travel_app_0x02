from celery import shared_task

@shared_task
def send_listing_email(listing_id):
    print(f"Sending email for listing {listing_id}")
    return f"Email sent for listing {listing_id}"