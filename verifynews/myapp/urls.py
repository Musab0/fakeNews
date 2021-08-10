
from django.urls import path

from . import views

urlpatterns = [
    path('user_page', views.user_page,name="user_page"),
    path('admin_page', views.admin_page, name='admin_page'),
    path('home_page', views.home_page, name='home_page'),
    # path('<str:phone_number>/',views.chat_page,name='chat_page'),
    path('<str:room_name>/', views.room, name='room'),

]