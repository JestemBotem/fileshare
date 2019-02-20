from django.urls import path, include

app_name = 'api'

urlpatterns = [
    path('link/', include('link.urls_api_v1', namespace='v1'))
]
