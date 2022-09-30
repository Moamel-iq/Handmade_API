from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver

from Handmade.utils.models import Entity


class EmailAccountManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})

    def create_user(self, first_name, last_name, email, password=None, **extra_fields):
        if not email:
            raise ValueError('user must have an email to register')

        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.first_name = first_name
        user.last_name = last_name
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class EmailAccount(AbstractUser):
    id = models.AutoField(primary_key=True)
    username = models.NOT_PROVIDED
    email = models.EmailField('Email Address', unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    is_verified = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = EmailAccountManager()

    def __str__(self):
        return self.email

    def update_password(self, old_password, new_password):
        if self.check_password(old_password):
            self.set_password(new_password)
            self.save()
            return True
        return False


class Profile(Entity):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(EmailAccount, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics', default='default.jpg')

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}{self.user.email}{self.user.phone_number}{self.user.address}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        return self.user.first_name + ' ' + self.user.last_name

    @property
    def email(self):
        return self.user.email

    @property
    def phone_number(self):
        return self.user.phone_number

    @property
    def address(self):
        return self.user.address

@receiver(post_save, sender=EmailAccount)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

