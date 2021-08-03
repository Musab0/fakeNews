from django.db import models
from django.db.models.base import ModelStateFieldsCacheDescriptor
from .validators import validate_file_extension

# Create your models here.
class Image(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    mediaType= models.Charfield(max_length=10) #image or video 
    image = models.ImageField(upload_to='images') # this will eventually be replpaced by filefield 
    # mediaFile= models.FileField(upload_to='images',validators=[validate_file_extension])
    date = models.DateTimeField(auto_now_add=True, blank=True)
    pdq = models.TextField()

    def __int__(self):
        return self.pk


    
    # hash_file_name = models.CharField(max_length=200)
    # classification= models.CharField(max_length=10, default="null")
    # def is_fake (self):
    #     return self.description
