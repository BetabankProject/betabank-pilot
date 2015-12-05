from django.contrib.auth.models import User
from django.db import models
from django_enumfield import enum


class SkillFamily(models.Model):
    """
    A broad family of skills eg Arts&Crafts, Business etc
    """
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)


class Skill(models.Model):
    """
    A detailed skill, that belongs to a :model:`models.SkillFamily`
    """
    family = models.ForeignKey(SkillFamily)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)


class Profile(models.Model):
    """
    Profile "extends" the :model:`auth.User` class with the additional fields that we need
    """
    # TODO add more fields
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    description = models.TextField('Description', max_length=5000)
    image = models.ImageField()
    skills = models.ManyToManyField(Skill)
    green_coins = models.PositiveSmallIntegerField('Green coin balance')
    blue_coins = models.PositiveSmallIntegerField('Blue coin balance')


class InitialCapital(models.Model):
    """
    This table holds the initial capital that the pioneer users have at moment T0
    (ie when the platform starts working).
    It will also be used when we show the complete history of a user's transactions.
    Additionally it can used to check the consistency of the system
    (by checking, the sum of all values of this table to the
    sum of the current balance of all users.
    """
    user = models.ForeignKey(User)
    value = models.PositiveSmallIntegerField()


# TODO elaborate more
class RequestStatus(enum.Enum):
    """
    Enum that defines the statuses in which a request can be.
    """
    OPEN = 'O'
    CANCELLED = 'C'
    MATCHED = 'M'
    FINISHED = 'F'

    _transitions = {
        OPEN: (CANCELLED, MATCHED,),
        CANCELLED: (),
        MATCHED: (CANCELLED, FINISHED, OPEN, ),
        FINISHED: (),

    }


class Request(models.Model):
    user = models.ForeignKey(User)
    date = models.DateTimeField("Date posted")
    description = models.TextField(max_length=2000)
    status = enum.EnumField(RequestStatus)


# TODO add transaction
