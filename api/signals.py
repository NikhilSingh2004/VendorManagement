from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from api.models import Vendor
from django.core.exceptions import ObjectDoesNotExist
import requests

@receiver(post_save, sender=Vendor)
def send_token_to_user(sender, instance, created, **kwargs):
    if created:
        try:
            response = requests.post(
                f"{settings.BASE_URL}/api/token/",
                data={
                    'username': instance.username,
                    'password': instance.password,
                }
            )
            if response.status_code == 200:
                # Successfully obtained token, extract it and save it to the user instance
                token = response.json().get('access')
                refresh = response.json().get('refresh')
                instance.auth_token = token
                instance.refresh = refresh
                instance.save()
        except Exception as e:
            print(f"Error sending token to user: {e}")
    else:
        # User is not created, it's an update (log in), you can handle this case here
        pass
