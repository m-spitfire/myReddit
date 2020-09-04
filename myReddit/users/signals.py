from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
from django.core.exceptions import ObjectDoesNotExist


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    try:
        instance.profile.save()
    except ObjectDoesNotExist:
        Profile.objects.create(user=instance)
