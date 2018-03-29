from django.db import models

# Create your models here.

from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.urls import reverse
from ecommerce.models import BookInstance
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    book_instance = models.ForeignKey(BookInstance, on_delete=models.CASCADE, blank=True
        , null=True, related_name='profiles')

    def __str__(self):
        return "@{}".format(self.user)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_profile(sender, instance, **kwargs):
    Profile.objects.get_or_create(user=instance, pk=instance.pk)
    instance.profile.save()

@receiver(pre_delete, sender=settings.AUTH_USER_MODEL)
def delete_profile(sender, instance, **kwargs):
    instance.profile.delete()

