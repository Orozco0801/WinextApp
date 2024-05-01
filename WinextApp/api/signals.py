from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from core.models import *

User = get_user_model()
#------------------------------------------------------------------------------------------------------------
# Create a profile when creating a user
#------------------------------------------------------------------------------------------------------------
@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        try:
            Profile.objects.create(user=instance)
        except IntegrityError:
            print("No se pudo crear el perfil. El usuario ya tiene un perfil.")

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
            print("No se pudo eliminar el perfil. El usuario no posee un perfil.")

#------------------------------------------------------------------------------------------------------------
# Create vehicle when creating profile
#------------------------------------------------------------------------------------------------------------
@receiver(post_save, sender=Profile)
def create_taxi_vehicle(sender, instance, created, **kwargs):
    if created and instance.user.role.name == "taxista":
        Vehicle.objects.create()