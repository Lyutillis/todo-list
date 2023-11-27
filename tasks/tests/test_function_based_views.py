from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from tasks.models import Task, Tag


def toggle_complete_url(pk) -> str:
    return reverse("tasks:task-toggle", args=[pk])


class PublicFunctionBasedViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.task = Task.objects.create(
            content="TestTask",
            deadline=timezone.now(),
            is_done=False,
        )

    def test_toggle_complete_view(self):
        response = self.client.get(toggle_complete_url(1))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.task.is_done)
        response = self.client.get(toggle_complete_url(1))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.task.is_done)
