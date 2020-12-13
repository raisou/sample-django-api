from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from clients.factories import UserFactory


class TaskAPITestCase(APITestCase):

    def setUp(self):
        self.user = UserFactory.create()

    def test_anonymous_list_tasks(self):
        response = self.client.get(reverse('tasks-list'))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_list_tasks(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(reverse('tasks-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
