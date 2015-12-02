from django.contrib.auth.models import User
from django.db import models


# Profile "extends" the User class from the contrib auth model with the additional fields that we need
class Profile(models.Model):
    user = models.OneToOneField(User)
    date_joined = models.DateTimeField('Profile creation date')
    description = models.CharField('Description', max_length=2000)
    # TODO add photo
    # TODO add more fields


# This table will hold the inital capital that each user has at moment T0 (when the platform starts working)
# It can then be used to check consistency of the system (by checking the sum of the current balance of all users
# to the sum of this table).
# It is also required if we want to show the history of a user's transactions.
class InitialCapital(models.Model):
    user = models.ForeignKey(User)
    value = models.IntegerField()


# Holds the current balance of green coins for all users
class GreenCoins(models.Model):
    user = models.ForeignKey(User)
    value = models.IntegerField()


# Holds the current balance of blue coins for all users
class BlueCoins(models.Model):
    user = models.ForeignKey(User)
    value = models.IntegerField()




