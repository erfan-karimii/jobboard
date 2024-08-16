from django.db.models.signals import post_save
from django.dispatch import receiver



from .models import UserProfile,User


@receiver(post_save, sender=User)
def create_profile_handler(sender, instance, created, **kwargs):
    print(instance)
    if created:
        if instance.role.role == "user":
            UserProfile.objects.create(user=instance)