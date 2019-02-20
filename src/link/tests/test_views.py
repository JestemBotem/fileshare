from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from freezegun import freeze_time

from link.models import ProtectedResource
from link.views import SecureUriView


class TestSecureUriView(TestCase):
    def setUp(self):
        self.user_name = 'testuser'
        self.user_password = 'testuserpass'
        self.user = User.objects.create_user(self.user_name, password=self.user_password)
        self.password_raw = 'my_super_secret_password_1337'

    def _fake_password(self):
        return self.password_raw

    def test_unauthenticated_access(self):
        response = self.client.get(reverse('link:new'))
        self.assertEqual(response.status_code, 302)

    def test_add_protected_link(self):
        example_link = 'http://example.com'

        self.client.login(username=self.user_name, password=self.user_password)

        with patch.object(SecureUriView, '_generate_password', self._fake_password):
            response = self.client.post(
                reverse('link:new'),
                data={'uri': example_link},
                follow=True
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ProtectedResource.objects.count(), 1)

        protected_resource = ProtectedResource.objects.all()[0]
        self.assertEqual(protected_resource.uri, example_link)
        self.assertTrue(protected_resource.is_valid_password(self.password_raw))
        self.assertContains(response, self.password_raw)

    def test_add_protected_file(self):
        self.client.login(username=self.user_name, password=self.user_password)

        example_content = b'examplefilefoobarxyz'

        with patch.object(SecureUriView, '_generate_password', self._fake_password):
            example_file = SimpleUploadedFile('example_file_name', example_content)

            response = self.client.post(
                reverse('link:new'),
                data={'file': example_file},
                follow=True
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ProtectedResource.objects.count(), 1)

        protected_resource = ProtectedResource.objects.all()[0]
        self.assertTrue(protected_resource.is_valid_password(self.password_raw))
        self.assertIsNone(protected_resource.uri)
        self.assertContains(response, self.password_raw)

    def test_add_protected_link_and_file(self):
        self.client.login(username=self.user_name, password=self.user_password)

        example_link = 'http://example.com'
        example_content = b'examplefilefoobarxyz'

        with patch.object(SecureUriView, '_generate_password', self._fake_password):
            example_file = SimpleUploadedFile('example_file_name', example_content)

            response = self.client.post(
                reverse('link:new'),
                data={
                    'uri': example_link,
                    'file': example_file,
                },
                follow=True
            )
        self.assertEqual(ProtectedResource.objects.count(), 0)
        self.assertContains(response, "Please select only URI or FILE to protect")


@freeze_time("2018-01-15 00:00:00")
class TestDownloadView(TestCase):
    def setUp(self):
        self.user_name = 'testuser'
        self.user_password = 'testuserpass'
        self.user = User.objects.create_user(self.user_name, password=self.user_password)
        self.invalid_uuid = '416927f6-d4ac-4532-b7dd-2334f3949815'
        self.resource_password = 'foopassword'
        self.protected_resource = ProtectedResource(
            user=self.user,
            uri='http://example.com'
        )
        self.protected_resource.set_password(self.resource_password)
        self.protected_resource.save()

    def test_no_resource(self):
        response = self.client.get(
            reverse('link:get', args=[self.invalid_uuid])
        )

        self.assertEqual(response.status_code, 404)

    @freeze_time("2018-01-16 00:00:00")
    def test_expired(self):
        response = self.client.get(
            reverse('link:get', kwargs={'id': self.protected_resource.id})
        )

        self.assertEqual(response.status_code, 404)

    def test_correct_password_link(self):
        response = self.client.post(
            reverse('link:get', kwargs={'id': self.protected_resource.id}),
            data={'password': self.resource_password},
        )

        self.assertRedirects(response, self.protected_resource.uri, fetch_redirect_response=False)

        updated_resource = ProtectedResource.objects.get(id=self.protected_resource.id)
        self.assertEqual(updated_resource.views_count, 1)

    def test_invalid_password_link(self):
        response = self.client.post(
            reverse('link:get', kwargs={'id': self.protected_resource.id}),
            data={'password': 'invalid_password'},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        updated_resource = ProtectedResource.objects.get(id=self.protected_resource.id)
        self.assertEqual(updated_resource.views_count, 0)
