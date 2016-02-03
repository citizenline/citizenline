from decimal import Decimal

from ckeditor.fields import RichTextField
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Avg, Count, Sum
from django.utils.translation import ugettext as _
from django_extensions.db.fields import RandomCharField
from model_utils.models import TimeStampedModel

from star_ratings.app_settings import STAR_RATINGS_RANGE


class Type(models.Model):
    name = models.CharField(_("name"), max_length=200)
    header = models.CharField(_("main header"), max_length=200)
    rating_header = models.CharField(_("rating header"), max_length=200, blank=True)
    comment_header = models.CharField(_("comment header"), max_length=200, blank=True)
    response_header = models.CharField(_("response header"), max_length=200, blank=True)
    rating_enabled = models.BooleanField(_("rating enabled"), default=True)
    comment_enabled = models.BooleanField(_("comment enabled"), default=True)
    notification_enabled = models.BooleanField(_("notification enabled"), default=True)

    class Meta:
        verbose_name = _('communication type')
        verbose_name_plural = _('communication types')

    def __str__(self):
        return self.name


class Text(models.Model):
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    title = models.CharField(_("title"), max_length=200)
    slug = RandomCharField(_("slug"), length=8, unique=True)
    body = RichTextField(_("text"), max_length=20000)
    version = models.PositiveIntegerField(default=0)
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    class Meta:
        verbose_name = _('text')
        verbose_name_plural = _('texts')

    def __str__(self):
        return '{}: {} ({})'.format(self.type, self.title, self.slug)

    def get_absolute_url(self):
        return "/improvetext/%s/" % self.slug


class Comment(models.Model):
    text = models.ForeignKey(Text)
    version = models.PositiveIntegerField(default=0)
    author = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    body = models.CharField(max_length=20000)
    notify = models.BooleanField(default=True)


# , editable=False
class Question(models.Model):
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    question = models.CharField(_("question"), max_length=200)
    position = models.IntegerField(_("position"))

    class Meta:
        verbose_name = _('question')
        verbose_name_plural = _('questions')

    def __str__(self):
        return self.question


class RatingManager(models.Manager):
    def for_instance(self, text, question):
        ratings, created = self.get_or_create(text=text, version=text.version, question=question)
        return ratings

    def rate(self, text, question, score, user, ip=None):
        rating, created = self.get_or_create(text=text, version=text.version, question=question)
        existing_rating = UserRating.objects.filter(user=user, rating=rating).first()
        if existing_rating:
            if getattr(settings, 'STAR_RATINGS_RERATE', True) is False:
                raise ValidationError(_('Already rated.'))
            existing_rating.score = score
            existing_rating.save()
            return existing_rating.rating
        else:
            return UserRating.objects.create(user=user, score=score, rating=rating, ip=ip).rating


class Rating(models.Model):
    """
    Attaches Rating models and running counts for a question on a version of the text.
    """
    count = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)
    average = models.DecimalField(max_digits=6, decimal_places=3, default=Decimal(0.0))

    text = models.ForeignKey(Text)
    version = models.PositiveIntegerField(default=0)
    question = models.ForeignKey(Question)

    objects = RatingManager()

    class Meta:
        unique_together = ['text', 'version', 'question']

    @property
    def percentage(self):
        return (self.average / STAR_RATINGS_RANGE) * 100

    def to_dict(self):
        return {
            'count': self.count,
            'total': self.total,
            'average': self.average,
            'percentage': self.percentage,
        }

    def calculate(self):
        """
        Recalculate the totals, and save.
        """
        aggregates = self.user_ratings.aggregate(total=Sum('score'), average=Avg('score'), count=Count('score'))
        self.count = aggregates.get('count') or 0
        self.total = aggregates.get('total') or 0
        self.average = aggregates.get('average') or 0.0
        self.save()


class UserRatingManager(models.Manager):

    def for_rating_by_id(self, text, question, id):
        return self.filter(rating__text=text, rating__question=question, user=id).first()


class UserRating(TimeStampedModel):
    """
    An individual rating of a user.
    """
    user = models.CharField(max_length=200)
    ip = models.GenericIPAddressField(blank=True, null=True)
    score = models.PositiveSmallIntegerField()
    rating = models.ForeignKey(Rating, related_name='user_ratings')

    objects = UserRatingManager()

    class Meta:
        unique_together = ['user', 'rating']

    def __str__(self):
        return '{} rating {} for {}'.format(self.user, self.score, self.rating.text)
