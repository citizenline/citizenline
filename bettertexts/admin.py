from __future__ import unicode_literals

from django.contrib import admin
# Register your models here.

from .models import Type
from .models import Text
from .models import Rating
from .models import UserRating
from .models import Question
from .models import TextComment
from django.http import HttpResponse
from django.contrib.sites.models import Site
from django.utils.translation import ugettext as _
from adminsortable2.admin import SortableInlineAdminMixin
from django_comments.admin import CommentsAdmin
import csv
from django.utils.encoding import smart_str


def export_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=mymodel.csv'
    writer = csv.writer(response, delimiter=str(u';'), quotechar=str(u'"'), quoting=csv.QUOTE_ALL)
    response.write(u'\ufeff'.encode('utf8'))  # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow([
        'ID',
        'Title',
        'Description',
    ])
    for obj in queryset:
        writer.writerow([
            smart_str(obj.pk),
            smart_str(obj.title),
            smart_str(obj.slug),
        ])
    return response

export_csv.short_description = 'Export CSV'


def export_coments(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=comments.csv'
    writer = csv.writer(response, delimiter=str(u';'), quotechar=str(u'"'), quoting=csv.QUOTE_ALL)
    response.write(u'\ufeff'.encode('utf8'))  # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow([
        'ID',
        'Title',
        'Name',
        'Email',
        'Inform',
        'Involved',
    ])
    for txt in queryset:
        for comment in TextComment.objects.for_model(model=txt):
            writer.writerow([
                smart_str(txt.slug),
                smart_str(txt.title),
                smart_str(comment.name),
                smart_str(comment.email),
                smart_str(comment.inform),
                smart_str(comment.involved),
            ])
    return response

export_coments.short_description = _('Export comments')


def export_rating(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=ratings.csv'
    writer = csv.writer(response, delimiter=b';', quotechar=b'"', quoting=csv.QUOTE_ALL)
    response.write(u'\ufeff'.encode('utf8'))  # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow([
        _('Text'),
        _('Version'),
        _('Question'),
        _('Score'),
        _('User'),
        _('IP'),
    ])
    for rating in queryset:
        for user_rating in UserRating.objects.filter(rating=rating):
            writer.writerow([
                smart_str(rating.text),
                smart_str(rating.version),
                smart_str(rating.question),
                smart_str(user_rating.score),
                smart_str(user_rating.user),
                smart_str(user_rating.ip),
            ])
    return response

export_rating.short_description = _('Export ratings')


# For models using site to always set current site
class SiteModelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.site = Site.objects.get_current()
        obj.save()


class TextAdmin(SiteModelAdmin):
    list_display = ('title', 'type', 'slug', 'version')
    list_filter = (
        'type__name',
    )
    actions = [export_csv, export_coments]
    pass


class QuestionInLine(SortableInlineAdminMixin, admin.TabularInline):
    model = Question
    extra = 0
    fieldsets = ((None, {'fields': ('question', 'position',)}),)
    ordering = ('position',)
    original = False


class TypeAdmin(SiteModelAdmin):

    list_display = ('name', 'rating_enabled', 'comment_enabled', 'notification_enabled',)

    fieldsets = (
        (None, {'fields': ('name', 'header',)}),
        (_('Headers'), {'fields': ('rating_header', 'comment_header', 'response_header',)}),
        (_('Enabled'), {'fields': ('rating_enabled', 'comment_enabled', 'notification_enabled',)}),
    )

    inlines = [QuestionInLine, ]

    class Media:
        css = {'all': ('bettertexts/css/hide_admin_original.css',)}


class RatingAdmin(SiteModelAdmin):
    list_display = ('text', 'version', 'question', 'range', 'count', 'total', 'average',)
    list_filter = ('text__type',)
    fieldsets = (
        (None, {'fields': ('text', 'version', 'question')}),
        (_('Score'), {'fields': ('range', 'count', 'total', 'average')})
    )
    readonly_fields = ('text', 'version', 'question', 'range', 'count', 'total', 'average',)

    actions = [export_rating,]

class UserRatingAdmin(SiteModelAdmin):
    list_display = ("rating", "score",)


class QuestionAdmin(admin.ModelAdmin):
    list_filter = ('type__name',)


class CommentsAdminText(CommentsAdmin):
    fieldsets = (
        (
            None,
            {'fields': ('content_type', 'object_pk')}
        ),
        (
            _('Content'),
            {'fields': ('user', 'user_name', 'user_email', 'user_url', 'comment')}
        ),
        (
            _('Metadata'),
            {'fields': ('submit_date', 'ip_address', 'is_public', 'is_removed')}
        ),
    )

    list_display = ('__str__', 'content_object', 'user_name', 'user_email', 'ip_address', 'submit_date', 'is_public', 'is_removed')
    list_filter = ('submit_date', 'is_public', 'is_removed')

    search_fields = ('comment', 'user_name', 'user_email', 'ip_address')
    actions = ["remove_comments"]

# my_admin_site = MyAdminSite()
admin.site.register(Text, TextAdmin)

admin.site.register(Type, TypeAdmin)
admin.site.register(TextComment, CommentsAdminText)
# admin.site.register(Question, QuestionAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(UserRating, UserRatingAdmin)

# Reset header  ?? Should this be done here or is this a sub-app ??
#admin.site.site_header = 'Citizenline admin'