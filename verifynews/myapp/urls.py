
from django.urls import path

from . import views

urlpatterns = [
    path('user_page', views.user_page,name="user_page"),
    path('admin_page', views.admin_page, name='admin_page'),
]