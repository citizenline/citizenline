from django.contrib import admin

# Register your models here.

from .models import Texttype
from .models import Improvetext

admin.site.register(Texttype)
admin.site.register(Improvetext)