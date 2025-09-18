from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.FetchProfileView.as_view(), name='fetch_profile'),
    path('fetch_db/', views.FetchFromDBView.as_view(), name='fetch_db'),
]