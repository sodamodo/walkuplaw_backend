from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_('Name of User'), blank=True, max_length=255)
    stripe_customer_id = models.CharField(_('stripe customer id'), blank=True, max_length=250)
    stripe_subscription_id = models.CharField(_('stripe subscription id'), max_length=250)
    stripe_subscription_paid_through = models.IntegerField(_('time stamp that the users is paid up through'),
                                                           blank=True, null=True)


    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})
