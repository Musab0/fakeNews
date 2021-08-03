from django.contrib import admin

# Register your models here.
from .models import Image

class ImageAdmin(admin.ModelAdmin):
    fields=['title', 'image','description','pdq','date',]
    readonly_fields=('date',)

admin.site.register(Image, ImageAdmin)

