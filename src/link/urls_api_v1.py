from django.urls import path
from rest_framework import routers

from link.apis import FileUploadView, DownloadView, ReportView

router = routers.DefaultRouter()
router.register(r'protected_resources', FileUploadView)

app_name = 'v1'

urlpatterns = [
    path('protected_resource', FileUploadView.as_view(), name='new'),
    path('protected_resource/<uuid:id>', DownloadView.as_view(), name='get'),
    path('report', ReportView.as_view(), name='report'),
]
