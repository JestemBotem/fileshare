from django.urls import path

from link.views import SecureUriView, DownloadView, CreatedView

app_name = 'link'

urlpatterns = [
    path('new/', SecureUriView.as_view(), name='new'),
    path('created/', CreatedView.as_view(), name='created'),
    path('download/<uuid:id>', DownloadView.as_view(), name='get'),

]
