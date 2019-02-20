from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('link/', include('link.urls', namespace='link')),
    path('api/v1/', include('fileshare.urls_api_v1', namespace='api'))
]
