from django.urls import path
from . import views
urlpatterns = [path('', views.sermon_list, name='sermon_list'), path('<int:pk>/', views.sermon_detail, name='sermon_detail')]
