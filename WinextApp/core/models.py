# Django imports
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext as _
from simple_history.models import HistoricalRecords

#------------------------------------------------------------------------------------------------------------
# Roles
#------------------------------------------------------------------------------------------------------------
class Role(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('Fecha de actualización', auto_now=True)
    deleted_at = models.DateTimeField('Fecha de eliminación', blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Rol'
        
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

    def restore(self, *args, **kwargs):
        self.is_deleted = False
        self.save()

#------------------------------------------------------------------------------------------------------------
# Administrador o super usuario
#------------------------------------------------------------------------------------------------------------
class UserManager(BaseUserManager):

    def _create_user(self, username, email, name, last_name, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            username=username,
            email=email,
            name=name,
            last_name=last_name,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, name, last_name, password=None, **extra_fields):
        return self._create_user(username, email, name, last_name, password, False, False, **extra_fields)

    def create_superuser(self, username, email, name, last_name, password=None, **extra_fields):
        return self._create_user(username, email, name, last_name, password, True, True, **extra_fields)

#------------------------------------------------------------------------------------------------------------
# Usuarios
#------------------------------------------------------------------------------------------------------------
class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField('Correo Electrónico', max_length=255, unique=True)
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, related_name='users', null=True, blank=True)
    
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        related_name='core_user_set',  
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        related_name='core_user_set',  
        related_query_name='user',
    )

    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('Fecha de actualización', auto_now=True)
    deleted_at = models.DateTimeField('Fecha de eliminación', blank=True, null=True)
    last_login = models.DateTimeField('Último inicio de sesión', auto_now=True)
    is_deleted = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return self.username

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.deleted_at = timezone.now() 
        self.save()

    def restore(self, *args, **kwargs):
        self.is_deleted = False
        self.save()

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

#------------------------------------------------------------------------------------------------------------
# Vehiculo
#------------------------------------------------------------------------------------------------------------
class Vehicle(models.Model):

    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    plate_number = models.CharField(unique=True, max_length= 20)

    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('Fecha de actualización', auto_now=True)
    deleted_at = models.DateTimeField('Fecha de eliminación', blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Vehicle'
        verbose_name_plural = 'Vehicles'

    def __str__(self):
        return f'{self.make} {self.model}'

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

    def restore(self, *args, **kwargs):
        self.is_deleted = False
        self.save()

#------------------------------------------------------------------------------------------------------------
# Agencia
#------------------------------------------------------------------------------------------------------------
class Agency(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True, max_length=30)

    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('Fecha de actualización', auto_now=True)
    deleted_at = models.DateTimeField('Fecha de eliminación', blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Agency")
        verbose_name_plural = _("Agencys")

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

    def restore(self, *args, **kwargs):
        self.is_deleted = False
        self.save()

    def get_absolute_url(self):
        return reverse("Agency_detail", kwargs={"pk": self.pk})


#------------------------------------------------------------------------------------------------------------
# Perfil
#------------------------------------------------------------------------------------------------------------
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField('Nombres', max_length=255, blank=True, null=True)
    last_name = models.CharField('Apellidos', max_length=255, blank=True, null=True)
    image = models.ImageField('Imagen de perfil', upload_to='perfil/', max_length=255, null=True, blank=True)
    phone_number = models.CharField('Número de teléfono', max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('Fecha de actualización', auto_now=True)
    deleted_at = models.DateTimeField('Fecha de eliminación', blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    historical = HistoricalRecords()

    def __str__(self):
        return self.name or f"Profile of {self.user.username}"

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

    def restore(self, *args, **kwargs):
        self.is_deleted = False
        self.save()

#------------------------------------------------------------------------------------------------------------
# Taxistas 
#------------------------------------------------------------------------------------------------------------
class TaxiUser(Profile):
    id_vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True)
    document = models.CharField(unique=True, max_length= 20)
    id_agency = models.OneToOneField(Agency, on_delete=models.SET_NULL, null=True)

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

    def restore(self, *args, **kwargs):
        self.is_deleted = False
        self.save()


#------------------------------------------------------------------------------------------------------------
# Viaje
#------------------------------------------------------------------------------------------------------------
class Trip(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_trips')
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='driver_trips')
    
    start_time = models.CharField(max_length=255)
    end_time = models.CharField(max_length=255)
    start_location = models.CharField(max_length=255)
    end_location = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Trip")
        verbose_name_plural = _("Trips")

    def __str__(self):
        return f'Trip from {self.start_location} to {self.end_location}'

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

    def restore(self, *args, **kwargs):
        self.is_deleted = False
        self.save()

    def get_absolute_url(self):
        return reverse("Trip_detail", kwargs={"pk": self.pk})


#--------------------------------
"""
class Rating(models.Model):
    id_rating = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()

class Configuration(models.Model):
    id_config = models.AutoField(primary_key=True)
    min_fare = models.DecimalField(max_digits=5, decimal_places=2)
    min_km = models.IntegerField()
    response_time = models.IntegerField()

class TripRequest(models.Model):
    id_request = models.AutoField(primary_key=True)
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_requests')
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='driver_requests')
    request_time = models.DateTimeField()
    start_location = models.PointField()
    end_location = models.PointField()
    accepted = models.BooleanField()
"""
