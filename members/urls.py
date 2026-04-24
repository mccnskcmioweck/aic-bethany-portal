from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('request/', views.service_request_create, name='service_request'),
    path('my-requests/', views.my_requests, name='my_requests'),
    path('list/', views.member_list, name='member_list'),
    path('<int:pk>/', views.member_detail, name='member_detail'),
    path('<int:pk>/edit/', views.member_edit, name='member_edit'),
    path('<int:pk>/approve/', views.approve_member, name='approve_member'),
    path('<int:pk>/reject/', views.reject_member, name='reject_member'),
    path('requests/', views.request_list, name='request_list'),
    path('requests/<int:pk>/manage/', views.request_manage, name='request_manage'),
]
