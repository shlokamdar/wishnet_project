from django.contrib import admin
from django.urls import path, include
from accounts import views as accounts_views  # Import the index view from the accounts app
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', accounts_views.index, name='index'),  # Map the root URL to the index view
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('friendship/', include('friendship.urls', namespace='friendship')),
    path('groups/', include('groups.urls', namespace='groups')),  
    path('wishlists/', include('wishlists.urls', namespace='wishlists')),  
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 