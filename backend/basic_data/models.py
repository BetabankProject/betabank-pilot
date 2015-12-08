from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django_enumfield import enum


class SkillFamily(models.Model):
    """
    A broad family of skills eg Arts&Crafts, Business etc
    """
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Skill Families"


class Skill(models.Model):
    """
    A detailed skill, that belongs to a :model:`models.SkillFamily`
    """
    family = models.ForeignKey(SkillFamily, verbose_name='Family')
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)

    def __str__(self):
        return "{} - {}".format(self.family.title, self.title)


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
    user = models.OneToOneField(User, verbose_name='User')
    value = models.PositiveSmallIntegerField()


# TODO elaborate more
class RequestStatus(enum.Enum):
    """
    Enum that defines the statuses in which a request can be.
    """
    OPEN = 0
    CANCELLED = 1
    MATCHED = 2
    FINISHED = 3

    # TODO add labels in a i18n way
    labels = {
        OPEN: 'OPEN',
    }

    _transitions = {
        OPEN: (CANCELLED, MATCHED,),
        CANCELLED: (),
        MATCHED: (CANCELLED, FINISHED, OPEN,),
        FINISHED: (),

    }


class RequestManager(models.Manager):
    """
    Creates a request and automatically sets 'date' to the current date
    and 'status' to OPEN
    """
    def create(self, user, json):
        request = Request(user=user,
                          title=json['title'],
                          description=json['description'],
                          hours=json['hours'],
                          category_id=json['category'],
                          date=timezone.now(),
                          status=RequestStatus.OPEN)
        request.save()


class Request(models.Model):
    """
    Represents a request of a service, placed by a user (an ad).
    Users that are interested in providing the requested service, can respond by placing an :model:`models.Offer`.
    The request can be for a fixed number of hours, or it can be an "open request", in which case the users
    can include the suggested amount of hours in their :model:`models.Offer`.
    """
    user = models.ForeignKey(User, verbose_name='Placed by')
    date = models.DateTimeField('Date posted')
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=2000)
    category = models.ForeignKey(SkillFamily)
    hours = models.PositiveSmallIntegerField('Number of hours required, 0 if open request')
    status = enum.EnumField(RequestStatus)
    objects = RequestManager()


class OfferStatus(enum.Enum):
    """
    Enum that defines the statuses in which a request can be
    """
    PLACED = 0
    CANCELLED = 1
    ACCEPTED = 2
    REJECTED = 3
    FINISHED = 4

    # TODO add labels in a i18n way
    labels = {
        PLACED: 'PLACED',
    }

    _transitions = {
        PLACED: (CANCELLED, ACCEPTED, REJECTED),
        ACCEPTED: (FINISHED,),
        CANCELLED: (),
        REJECTED: (),
        FINISHED: (),
    }


class Offer(models.Model):
    """
    An offer is a response to a :model:`models.Request`, placed by a user who is willing to offer the
    service that is requested.
    If the request was an open one, the user must provide the number of hours.
    """
    placedBy = models.ForeignKey(User, verbose_name='Placed by')
    date = models.DateTimeField('Date placed')
    request = models.ForeignKey(Request)
    description = models.TextField(max_length=2000)
    hours = models.PositiveSmallIntegerField('Number of hours (only to be filled if the offer is for an open request)')
    status = enum.EnumField(OfferStatus)
