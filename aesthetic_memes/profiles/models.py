from django.db import models

# Create your models here.

from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.urls import reverse
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    ALABAMA = 'AL'; ALASKA = 'AK'; ARIZONA = 'AZ'; ARKANSAS = 'AR'; CALIFORNIA = 'CA'
    COLORADO = 'CO'; CONNECTICUT = 'CT'; DELAWARE = 'DE'; FLORIDA = 'FL'; GEORGIA = 'GA'
    HAWAII = 'HI'; IDAHO = 'ID'; ILLINOIS = 'IL'; INDIANA = 'IN'; IOWA = 'IA'; KANSAS = 'KS'
    KENTUCKY = 'KY'; LOUISIANA = 'LA'; MAINE = 'ME'; MARYLAND = 'MD'; MASSACHUSETTS = 'MA'
    MICHIGAN = 'MI'; MINNESOTA = 'MN'; MISSISSIPPI = 'MS'; MISSOURI = 'MO'; MONTANA = 'MT'
    NEBRASKA = 'NE'; NEVADA = 'NV'; NEW_HAMPSHIRE = 'NH'; NEW_JERSEY = 'NJ'; NEW_MEXICO = 'NM'
    NEW_YORK = 'NY'; NORTH_CAROLINA = 'NC'; NORTH_DAKOTA = 'ND'; OHIO = 'OH'; OKLAHOMA = 'OK'
    OREGON = 'OR'; PENNSYLVANIA = 'PA'; RHODE_ISLAND = 'RI'; SOUTH_CAROLINA = 'SC'; SOUTH_DAKOTA = 'SD'
    TENNESSEE = 'TN'; TEXAS = 'TX'; UTAH = 'UT'; VERMONT = 'VT'; VIRGINIA = 'VA'; WASHINGTON = 'WA';
    WEST_VIRGINIA = 'WV'; WISCONSIN = 'WI'; WYOMING = 'WY'; DISTRICT_OF_COLUMBIA = 'DC'

    STATE_CHOICES = (
        (ALABAMA, 'Alabama'), (ALASKA, 'Alaska'), (ARIZONA, 'Arizona'), (ARKANSAS, 'Arkansas'), (CALIFORNIA, 'California'),
        (COLORADO, 'Colorado'), (CONNECTICUT, 'Connecticut'), (DELAWARE, 'Delaware'), (FLORIDA, 'Florida'), (GEORGIA, 'Georgia'),
        (HAWAII, 'Hawaii'), (IDAHO, 'Idaho'), (ILLINOIS, 'Illinois'), (INDIANA, 'Indiana'), (IOWA, 'Iowa'), (KANSAS, 'Kansas'),
        (KENTUCKY, 'Kentucky'), (LOUISIANA, 'Louisiana'), (MAINE, 'Maine'), (MARYLAND, 'Maryland'), (MASSACHUSETTS, 'Massachusetts'),
        (MICHIGAN, 'Michigan'), (MINNESOTA, 'Minnesota'), (MISSISSIPPI, 'Mississippi'), (MISSOURI, 'Missouri'), (MONTANA, 'Montana'),
        (NEBRASKA, 'Nebraska'), (NEVADA, 'Nevada'), (NEW_HAMPSHIRE, 'New Hampshire'), (NEW_JERSEY, 'New Jersey'), (NEW_MEXICO, 'New Mexico'),
        (NEW_YORK, 'New York'), (NORTH_CAROLINA, 'North Carolina'), (NORTH_DAKOTA, 'North Dakota'), (OHIO, 'Ohio'), (OKLAHOMA, 'Oklahoma'),
        (OREGON, 'Oregon'), (PENNSYLVANIA, 'Pennsylvania'), (RHODE_ISLAND, 'Rhode Island'), (SOUTH_CAROLINA, 'South Carolina'), (SOUTH_DAKOTA, 'South Dakota'),
        (TENNESSEE, 'Tennessee'), (TEXAS, 'Texas'), (UTAH, 'Utah'), (VERMONT, 'Vermont'), (VIRGINIA, 'Virginia'), (WASHINGTON, 'Washington'),
        (WEST_VIRGINIA, 'West Virginia'), (WISCONSIN, 'Wisconsin'), (WYOMING, 'Wyoming'), (DISTRICT_OF_COLUMBIA, 'District of Columbia'),
    )

    first_name = models.CharField(max_length=100, default='', blank=False)
    last_name = models.CharField(max_length=100, default='', blank=False)

    address = models.CharField(max_length=100, default='', blank=False)
    city = models.CharField(max_length=30, default='', blank=False)
    state = models.CharField(max_length=2, default='', choices=STATE_CHOICES, blank=False)
    zip_code = models.CharField(max_length=10, default='', blank=False)

    phone_number = models.CharField(default='', max_length=15, blank=True)

    def __str__(self):
        return "@{}".format(self.user)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_profile(sender, instance, **kwargs):
    Profile.objects.get_or_create(user=instance, pk=instance.pk)
    instance.profile.save()

@receiver(pre_delete, sender=settings.AUTH_USER_MODEL)
def delete_profile(sender, instance, **kwargs):
    instance.profile.delete()

