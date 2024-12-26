from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'accounts'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('login/forgot_password/', views.forgot_password, name='forgot_password'),
    path('verify_otp/', views.verify_otp, name="verify_otp"),
    path('reset_password/<int:user_id>/', views.reset_password, name='reset_password'), 
    path('dashboard/', views.dashboard, name='dashboard'),  # Ensure the trailing slash is present
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('view_profile/<int:user_id>/', views.view_profile, name='view_profile'),  # Profile page
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
