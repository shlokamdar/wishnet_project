from django.urls import path
from . import views

app_name = 'wishlists'

urlpatterns = [
    path('create/', views.create_wishlist, name='create_wishlist'),
    path('wishlist_list/<int:user_id>/', views.wishlist_list, name='wishlist_list'),  # Added user_id here
    path('wishlist_detail/<int:pk>/', views.wishlist_detail, name='wishlist_detail'),
    path('<int:pk>/edit/', views.edit_wishlist, name='edit_wishlist'),
    path('wishlist/<int:wishlist_id>/add-item/', views.add_item, name='add_item'),
    path('item/<int:pk>/edit/', views.edit_item, name='edit_item'),
    path('item/<int:pk>/delete/', views.delete_item, name='delete_item'),
    path('<int:wishlist_id>/share/', views.share_wishlist, name='share_wishlist'),
]
