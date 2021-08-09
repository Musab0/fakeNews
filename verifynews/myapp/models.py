from django.db import models
from django.db.models.base import ModelStateFieldsCacheDescriptor
from django.db.models.deletion import CASCADE
from django.db.models.fields import BooleanField
from .validators import validate_file_extension, file_type

# Create your models here.
# class Image(models.Model):
#     STATUS=(
#         ('real', ('Real')),
#         ('fake', ('Fake')),
#         ('unsorted', ('Unsorted')),
#     )

#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     # mediaType= models.CharField(max_length=10) #image or video 
#     image = models.ImageField(upload_to='images') # this will eventually be replpaced by filefield 
#     # mediaFile= models.FileField(upload_to='images',validators=[validate_file_extension])
#     date = models.DateTimeField(auto_now_add=True, blank=True)
#     category=models.CharField(max_length=20,choices=STATUS, default='unsorted')
#     pdq = models.TextField()

#     def __int__(self):
#         return self.pk


class Image(models.Model):  # changed ImgField to FileField 
    STATUS=(
        ('real', ('Real')),
        ('fake', ('Fake')),
        ('unsorted', ('Unsorted')),
    )

    FILE_TYPE=(
        ('image', ('Image')),
        ('video', ('Video')),
        ('unknown', ('Unknown')),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    # mediaType= models.CharField(max_length=10) #image or video 
    image = models.FileField(upload_to='images',validators=[validate_file_extension]) # this will eventually be replpaced by filefield 
    # mediaFile= models.FileField(upload_to='images',validators=[validate_file_extension])
    date = models.DateTimeField(auto_now_add=True, blank=True)
    category=models.CharField(max_length=20,choices=STATUS, default='unsorted')
    pdq = models.TextField()
    fileType=models.CharField(max_length=20,choices=FILE_TYPE, default='unknown')

    def set_fileType(self):
        self.fileType=file_type(self.image.name)

    def __int__(self):
        return self.pk



class User(models.Model):

    phone = models.CharField(max_length=15)
    Image = models.ManyToManyField(Image, through='Upload')
    #use this later to follow the standard way of storing phone numbers (requires dependency)
    # phone = models.PhoneNumberField(null=False, blank=False, unique=True)   

    def __str__(self):
        return self.phone


class Upload(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    image=models.ForeignKey(Image, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, blank=True)
