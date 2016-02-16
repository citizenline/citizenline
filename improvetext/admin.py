from __future__ import unicode_literals

from django.contrib import admin
# Register your models here.

from .models import Type
from .models import Text
from .models import UserRating
from .models import Question
from django.http import HttpResponse
from django.contrib.sites.models import Site
from django.utils.translation import ugettext as _


def export_csv(modeladmin, request, queryset):
    import csv
    from django.utils.encoding import smart_str
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=mymodel.csv'
    writer = csv.writer(response, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
    response.write(u'\ufeff'.encode('utf8'))  # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow([
        "ID",
        "Title",
        "Description",
    ])
    for obj in queryset:
        writer.writerow([
            smart_str(obj.pk),
            smart_str(obj.title),
            smart_str(obj.slug),
        ])
    return response


export_csv.short_description = "Export CSV"


# For models using site to always set current site
class SiteModelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.site = Site.objects.get_current()
        obj.save()


class TextAdmin(SiteModelAdmin):
    list_display = ("title", "type", "slug", "version")
    list_filter = (
        'type__name',
    )
    actions = [export_csv]
    pass


class QuestionInLine(admin.TabularInline):
    model = Question
    extra = 0


class TypeAdmin(SiteModelAdmin):
    list_display = ("name", "rating_enabled", "comment_enabled", "notification_enabled",)
    list_filter = ('site__name',)

    inlines = [
        QuestionInLine
    ]

    fieldsets = (
        (None, {'fields': ('name', 'header')}),
        (_('Headers'), {'fields': ('rating_header', 'comment_header', 'response_header',)}),
        (_('Enabled'), {'fields': ('rating_enabled', 'comment_enabled', 'notification_enabled',)}),
    )


class QuestionAdmin(admin.ModelAdmin):
    list_filter = ('type__name',)


# my_admin_site = MyAdminSite()
admin.site.register(Text, TextAdmin)

admin.site.register(Type, TypeAdmin)
# admin.site.register(Comment)
# admin.site.register(Question, QuestionAdmin)
# admin.site.register(Rating)
admin.site.register(UserRating)

# Reset header  ?? Should this be done here or is this a sub-app ??
admin.site.site_header = 'Citizenline admin'