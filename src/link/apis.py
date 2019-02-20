from django.http import Http404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404, CreateAPIView, ListAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from link.models import ProtectedResource
from link.serializers import ProtectedResourceSerializer, PasswordSerializer, ReportSerializer


class FileUploadView(CreateAPIView):
    parser_classes = (MultiPartParser,)
    queryset = ProtectedResource.objects.all()
    serializer_class = ProtectedResourceSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DownloadView(CreateAPIView):
    serializer_class = PasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.protected_resource = get_object_or_404(ProtectedResource, pk=self.kwargs['id'])

        if not self.protected_resource.is_available():
            raise Http404()

        if not self.protected_resource.is_valid_password(serializer.validated_data['password']):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        headers = self.get_success_headers(serializer.data)

        status_code = status.HTTP_307_TEMPORARY_REDIRECT
        if self.protected_resource.file is not None:
            status_code = status.HTTP_200_OK

        return Response('', status=status_code, headers=headers)

    def get_success_headers(self, data):
        if self.protected_resource.file is not None:
            return {
                'X-Accel-Redirect': '/uploads/' + self.protected_resource.file_name,
                'Content-Disposition': 'attachment; filename=%s' % self.protected_resource.file_name,
                'Content-Type': '',
            }

        return {'Location': self.protected_resource.uri}


class ReportView(ListAPIView):
    serializer_class = ReportSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        return ProtectedResource.objects.get_access_report()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
