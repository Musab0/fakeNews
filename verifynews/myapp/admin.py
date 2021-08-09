from django.contrib import admin

# Register your models here.
from .models import Image, Upload, User

class ImageAdmin(admin.ModelAdmin):
    fields=['title', 'image','description','pdq','date','user','fileType']
    readonly_fields=('date','fileType')

class UserAdmin(admin.ModelAdmin):
    fields=['phone','Image',]


# admin.site.register(Image, ImageAdmin)
admin.site.register(Image)
# admin.site.register(User, UserAdmin)
admin.site.register(User)
admin.site.register(Upload)
