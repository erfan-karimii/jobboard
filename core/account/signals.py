from django.db.models.signals import post_save
from django.dispatch import receiver



from .models import UserProfile,User,CompanyProfile


@receiver(post_save, sender=User)
def create_profile_handler(sender, instance, created, **kwargs):
    if created:
        if instance.role.role == "user":
            UserProfile.objects.create(user=instance)
        elif instance.role.role == "company":
            CompanyProfile.objects.create(user=instance,employee_number=0)

