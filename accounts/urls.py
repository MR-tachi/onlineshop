from django.urls import path, include
from . import views

urlpatterns = [
    path('profile', views.profile, name='profile'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('profile/<str:edit>', views.profile, name='profile'),

]
