from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()
#------------------------------------------------------------------------------------------------------------
# Create a profile when creating a user
#------------------------------------------------------------------------------------------------------------
@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

#------------------------------------------------------------------------------------------------------------
# Delete Profile when deleting user
#------------------------------------------------------------------------------------------------------------
@receiver(post_save, sender=User)
def update_profile_status(sender, instance, **kwargs):
    if instance.is_deleted:
        try:
            profile = Profile.objects.get(user=instance)
            profile.is_deleted = True
            profile.save()
        except Profile.DoesNotExist:
            # Manejar el caso donde no existe un perfil, opcional
            pass