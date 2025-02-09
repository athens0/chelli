from django.urls import path
from . import views

app_name = 'anigesser'

urlpatterns = [
    path('', views.home, name='home'),
    path('news/', views.news, name='news'),
    path('calendar/', views.calendar, name='calendar'),
    path('ratings/', views.ratings, name='ratings'),
    path('about/', views.about, name='about'),
    path('licence/', views.licence, name='licence'),
    path('titles/<int:page>', views.titles, name='titles'),
    path('suggest/', views.suggest, name='suggest'),
    path('contacts/', views.contacts, name='contacts'),
    path('title/<int:id>', views.title, name='title'),
    path('register/', views.register, name='register'),
    path('register/verify/', views.verify, name='verify'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile, name='profile'),
    path('profile/exit', views.exit, name='exit'),
]
