
from django.urls import path

from . import views

urlpatterns = [
    path('user_page', views.user_page),
    # path('admin_page', views.index, name='index'),
]