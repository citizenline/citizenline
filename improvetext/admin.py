from __future__ import unicode_literals
from django.contrib import admin

# Register your models here.

from .models import Type
from .models import Text
from .models import Comment
from .models import Rating
from .models import UserRating
from .models import Question
from django.http import HttpResponse


def export_csv(modeladmin, request, queryset):
    import csv
    from django.utils.encoding import smart_str
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=mymodel.csv'
    writer = csv.writer(response, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
    response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
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


class TextAdmin(admin.ModelAdmin):
    actions = [export_csv]
    pass
admin.site.register(Text, TextAdmin)

admin.site.register(Type)
admin.site.register(Comment)
admin.site.register(Question)
admin.site.register(Rating)
admin.site.register(UserRating)
