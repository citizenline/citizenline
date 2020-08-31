from decimal import Decimal

from ckeditor.fields import RichTextField
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Avg, Count, Sum
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django_comments.managers import CommentManager
from django_comments.models import BaseCommentAbstractModel
from django_extensions.db.fields import RandomCharField
from model_utils.models import TimeStampedModel

from star_ratings.app_settings import STAR_RATINGS_RANGE

COMMENT_MAX_LENGTH = getattr(settings, "COMMENT_MAX_LENGTH", 3000)


@python_2_unicode_compatible
class TextComment(BaseCommentAbstractModel):
    """
    A user comment about text.
    """

    # Who posted this comment? If ``user`` is set then it was an authenticated
    # user; otherwise at least user_name should have been set and the comment
    # was posted by a non-authenticated user.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("user"),
        blank=True,
        null=True,
        related_name="%(class)s_comments",
        on_delete=models.CASCADE,
    )
    user_name = models.CharField(_("user's name"), max_length=50, blank=True)
    # Explicit `max_length` to apply both to Django 1.7 and 1.8+.
    user_email = models.EmailField(
        _("user's email address"), max_length=254, blank=True
    )
    user_url = models.URLField(_("user's URL"), blank=True)
    inform = models.BooleanField(
        _("Keep informed"),
        default=False,
        help_text=_("Check this box to keep me informed " "about updates."),
    )
    involved = models.BooleanField(
        _("Stay involved"),
        default=False,
        help_text=_("Check this box to make more texts " "better."),
    )

    comment = models.TextField(_("comment"), max_length=COMMENT_MAX_LENGTH)

    # Metadata about the comment
    submit_date = models.DateTimeField(_("date/time submitted"), default=None)
    ip_address = models.GenericIPAddressField(
        _("IP address"), unpack_ipv4=True, blank=True, null=True
    )
    is_public = models.BooleanField(
        _("is public"),
        default=True,
        help_text=_(
            "Uncheck this box to make the comment effectively "
            "disappear from the site."
        ),
    )
    is_removed = models.BooleanField(
        _("is removed"),
        default=False,
        help_text=_(
            "Check this box if the comment is inappropriate. "
            'A "This comment has been removed" message will '
            "be displayed instead."
        ),
    )

    # Manager
    objects = CommentManager()

    class Meta:
        # db_table = "django_comments"
        ordering = ("submit_date",)
        permissions = [("can_moderate", "Can moderate comments")]
        verbose_name = _("comment")
        verbose_name_plural = _("comments")

    def __str__(self):
        return "%s: %s..." % (self.name, self.comment[:50])

    def save(self, *args, **kwargs):
        if self.submit_date is None:
            self.submit_date = timezone.now()
        super(TextComment, self).save(*args, **kwargs)

    def _get_userinfo(self):
        """
        Get a dictionary that pulls together information about the poster
        safely for both authenticated and non-authenticated comments.

        This dict will have ``name``, ``email``, and ``url`` fields.
        """
        if not hasattr(self, "_userinfo"):
            userinfo = {
                "name": self.user_name,
                "email": self.user_email,
                "url": self.user_url,
            }
            if self.user_id:
                u = self.user
                if u.email:
                    userinfo["email"] = u.email

                # If the user has a full name, use that for the user name.
                # However, a given user_name overrides the raw user.username,
                # so only use that if this comment has no associated name.
                if u.get_full_name():
                    userinfo["name"] = self.user.get_full_name()
                elif not self.user_name:
                    userinfo["name"] = u.get_username()
            self._userinfo = userinfo
        return self._userinfo

    userinfo = property(_get_userinfo, doc=_get_userinfo.__doc__)

    def _get_name(self):
        return self.userinfo["name"]

    def _set_name(self, val):
        if self.user_id:
            raise AttributeError(
                _(
                    "This comment was posted by an authenticated "
                    "user and thus the name is read-only."
                )
            )
        self.user_name = val

    name = property(
        _get_name, _set_name, doc="The name of the user who posted this comment"
    )

    def _get_email(self):
        return self.userinfo["email"]

    def _set_email(self, val):
        if self.user_id:
            raise AttributeError(
                _(
                    "This comment was posted by an authenticated "
                    "user and thus the email is read-only."
                )
            )
        self.user_email = val

    email = property(
        _get_email, _set_email, doc="The email of the user who posted this comment"
    )

    def _get_url(self):
        return self.userinfo["url"]

    def _set_url(self, val):
        self.user_url = val

    url = property(
        _get_url, _set_url, doc="The URL given by the user who posted this comment"
    )

    def get_absolute_url(self, anchor_pattern="#c%(id)s"):
        return self.get_content_object_url() + (anchor_pattern % self.__dict__)

    def get_as_text(self):
        """
        Return this comment as plain text.  Useful for emails.
        """
        d = {
            "user": self.user or self.name,
            "date": self.submit_date,
            "comment": self.comment,
            "domain": self.site.domain,
            "url": self.get_absolute_url(),
        }
        return (
            _(
                "Posted by %(user)s at %(date)s\n\n%(comment)s\n\nhttp://%(domain)s%(url)s"
            )
            % d
        )


class TypeManager(CurrentSiteManager):
    def get_query_set(self):
        return super(TypeManager, self).get_query_set()


class Type(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    objects = TypeManager()
    on_site = CurrentSiteManager()
    name = models.CharField(_("name"), max_length=200)
    header = models.CharField(_("main header"), max_length=200)
    rating_header = models.CharField(_("rating header"), max_length=200, blank=True)
    comment_header = models.CharField(_("comment header"), max_length=200, blank=True)
    response_header = models.CharField(_("response header"), max_length=200, blank=True)
    rating_enabled = models.BooleanField(_("rating enabled"), default=True)
    comment_enabled = models.BooleanField(_("comment enabled"), default=True)
    notification_enabled = models.BooleanField(_("notification enabled"), default=True)
    comment_form_intro = models.TextField(_("comment form intro"), max_length=20000, blank=True)

    class Meta:
        verbose_name = _("communication type")
        verbose_name_plural = _("communication types")

    def __str__(self):
        return self.name


class Text(models.Model):
    site = models.ForeignKey(Site, default=1, editable=False, on_delete=models.CASCADE)
    objects = TypeManager()
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    title = models.CharField(_("title"), max_length=200)
    slug = RandomCharField(_("slug"), length=8, unique=True)
    intro = RichTextField(_("intro"), max_length=20000, blank=True)
    body = RichTextField(_("text"), max_length=20000)
    version = models.PositiveIntegerField(_("version"), default=0)
    pub_date = models.DateTimeField(_("date published"), auto_now_add=True)
    end_date = models.DateTimeField(_("date end"), blank=True, null=True)
    comments = GenericRelation(TextComment, object_id_field="object_pk")

    class Meta:
        verbose_name = _("text")
        verbose_name_plural = _("texts")

    def __str__(self):
        return "{}: {} ({})".format(self.type, self.title, self.slug)

    def get_absolute_url(self):
        return "/bettertexts/%s/" % self.slug

    def active(self):
        return self.end_date is None or timezone.now() <= self.end_date


# , editable=False
class Question(models.Model):
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    question = models.CharField(_("question"), max_length=200)
    position = models.IntegerField(_("position"))

    class Meta:
        verbose_name = _("question")
        verbose_name_plural = _("questions")
        ordering = ("position",)

    def __str__(self):
        return self.question


class RatingManager(models.Manager):
    def for_instance(self, text, question):
        ratings, created = self.get_or_create(
            text=text, version=text.version, question=question
        )
        return ratings

    def rate(self, text, question, score, user, ip=None):
        rating = self.get_or_create(text=text, version=text.version, question=question)[
            0
        ]
        existing_rating = UserRating.objects.filter(user=user, rating=rating).first()
        if existing_rating:
            if getattr(settings, "STAR_RATINGS_RERATE", True) is False:
                raise ValidationError(_("Already rated."))
            existing_rating.score = score
            existing_rating.ip = ip
            existing_rating.save()
            return existing_rating.rating
        else:
            return UserRating.objects.create(
                user=user, score=score, rating=rating, ip=ip
            ).rating


class Rating(models.Model):
    """
    Attaches Rating models and running counts for a question on a version of the text.
    """

    text = models.ForeignKey(Text, on_delete=models.CASCADE)
    version = models.PositiveIntegerField(_("version"), default=0)
    question = models.ForeignKey(
        Question, verbose_name=_("Question"), on_delete=models.CASCADE
    )

    range = models.PositiveIntegerField(_("range"), default=STAR_RATINGS_RANGE)
    count = models.PositiveIntegerField(_("count"), default=0)
    total = models.PositiveIntegerField(_("total"), default=0)
    average = models.DecimalField(
        _("average"), max_digits=6, decimal_places=2, default=Decimal(0.0)
    )

    objects = RatingManager()

    class Meta:
        unique_together = ["text", "version", "question"]
        verbose_name = _("rating")
        verbose_name_plural = _("ratings")

    def __str__(self):
        return "{} [{}]: {}".format(self.text.title, self.version, self.question)

    @property
    def percentage(self):
        return (self.average / self.range) * 100

    def to_dict(self):
        return {
            "count": self.count,
            "total": self.total,
            "average": self.average,
            "percentage": self.percentage,
        }

    def calculate(self):
        """
        Recalculate the totals, and save.
        """
        aggregates = self.user_ratings.aggregate(
            total=Sum("score"), average=Avg("score"), count=Count("score")
        )
        self.count = aggregates.get("count") or 0
        self.total = aggregates.get("total") or 0
        self.average = aggregates.get("average") or 0.0
        self.save()


class UserRatingManager(models.Manager):
    def for_rating_by_id(self, text, question, uid):
        return self.filter(
            rating__text=text, rating__question=question, user=uid
        ).first()


class UserRating(TimeStampedModel):
    """
    An individual rating of a user.
    """

    user = models.CharField(max_length=200)
    ip = models.GenericIPAddressField(blank=True, null=True)
    score = models.PositiveSmallIntegerField()
    rating = models.ForeignKey(
        Rating, related_name="user_ratings", editable=False, on_delete=models.CASCADE
    )

    objects = UserRatingManager()

    class Meta:
        unique_together = ["user", "rating"]

    def __str__(self):
        return "{} rating {} for {}".format(self.user, self.score, self.rating.text)
