from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from clients.factories import UserFactory

from .models import Task


class TaskAPITestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory.create()

    def test_anonymous_list_tasks(self):
        response = self.client.get(reverse("tasks-list"))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_create_tasks(self):
        response = self.client.post(reverse("tasks-list"), {"task_type": Task.HEAVY})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_list_tasks(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(reverse("tasks-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_create_light_task(self):
        self.client.force_authenticate(user=self.user)

        data = {"task_type": Task.LIGHT}

        response = self.client.post(reverse("tasks-list"), data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Initial load is async coz data are empty
        self.assertEqual(response.data.get("execution_type"), Task.ASYNC)

        response = self.client.post(reverse("tasks-list"), data)
        # 2nd run is ok (coz these task duration is fixed)
        self.assertEqual(response.data.get("execution_type"), Task.SYNC)

    def test_user_create_heavy_task(self):
        self.client.force_authenticate(user=self.user)

        data = {"task_type": Task.HEAVY}

        response = self.client.post(reverse("tasks-list"), data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("execution_type"), Task.ASYNC)

    def test_user_create_random_task(self):
        self.client.force_authenticate(user=self.user)

        data = {"task_type": Task.RANDOM}

        response = self.client.post(reverse("tasks-list"), data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_create_random_task_with_treshold(self):
        # TODO
        pass

    def test_user_list_only_his_own_tasks(self):
        # TODO
        pass

    def test_user_retrieve_only_his_own_tasks(self):
        # TODO
        pass

    def test_user_create_heavy_task_async(self):
        # TODO
        pass

    def test_user_create_light_task_sync(self):
        # TODO
        pass

    def test_user_create_random_task_treshold(self):
        # TODO
        pass

    def test_user_retrieve_result_from_async_task(self):
        # TODO
        pass

    def test_user_retrieve_result_from_sync_task(self):
        # TODO
        pass

    def test_user_get_result_from_async_task(self):
        # TODO
        pass

    def test_user_get_result_from_sync_task(self):
        # TODO
        pass
