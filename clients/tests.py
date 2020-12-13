from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .factories import UserFactory


class ClientAPITestCase(APITestCase):

    def setUp(self):
        self.admin = UserFactory.create(is_staff=True)

    def test_anonymous_access_admin_endpoint(self):
        response = self.client.get(reverse('clients-list'))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_access_admin_endpoint(self):
        user = UserFactory.create(is_staff=False)

        self.client.force_authenticate(user=user)

        response = self.client.get(reverse('clients-list'))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_access_admin_endpoint(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.get(reverse('clients-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_clients_list_result(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.get(reverse('clients-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get('total_calls'), 0)
