from django.urls import path
from . import views

app_name = 'groups'

urlpatterns = [
    path('create_group/', views.create_group, name='create_group'),
    path('join_group/', views.join_group, name='join_group'),
    path('group_detail/<int:group_id>/', views.group_detail, name='group_detail'),
    path('group/<int:group_id>/remove_member/', views.remove_member, name='remove_member'),
    path('user-groups/', views.user_groups, name='user_groups'),
    path('group/<int:group_id>/add_wishlist/', views.add_wishlist_to_group, name='add_wishlist_to_group'),
    path('group/<int:group_id>/assign_secret_santa/', views.assign_secret_santa, name='assign_secret_santa'),
]
