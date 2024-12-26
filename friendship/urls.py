# urls.py
from django.urls import path
from . import views

app_name = 'friendship' 

urlpatterns = [
    # Friendship URLs
    path('send_friend_request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('remove_friend/<int:user_id>/', views.remove_friend, name='remove_friend'),
    path('view_friend_requests/', views.view_friend_requests, name='view_friend_requests'),
    path('accept_friend_request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('reject_friend_request/<int:request_id>/', views.reject_friend_request, name='reject_friend_request'),
    path('search/', views.search_user, name='search_user'),  
]
