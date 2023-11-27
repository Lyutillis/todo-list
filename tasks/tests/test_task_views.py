from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from tasks.models import Tag, Task

TASKS_URL = reverse("tasks:task-list")


class PublicTagTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tag = Tag.objects.create(
            name="TestTag"
        )
        number_of_tasks = 23

        for task_id in range(number_of_tasks):
            Task.objects.create(
                content=f"Task {task_id}",
                deadline=timezone.now(),
            )

    def test_retrieve_tasks(self):
        response = self.client.get(TASKS_URL)
        self.assertEqual(response.status_code, 200)
        tasks = Task.objects.all()
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["task_list"]), 4)
        self.assertEqual(list(response.context["task_list"]), list(tasks)[:4])
        self.assertTemplateUsed(response, "tasks/task_list.html")

    def test_retrieve_tasks_last_page(self):
        response = self.client.get(TASKS_URL + "?page=6")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["task_list"]), 3)

    def test_create_task(self):
        form_data = {
            "content": "TestTask",
            "deadline": timezone.now(),
            "tags": [self.tag.pk],
        }
        self.client.post(reverse("tasks:task-create"), data=form_data)

        new_task = Task.objects.filter(content=form_data["content"]).first()

        self.assertIsNotNone(new_task)
        self.assertEqual(
            [tag.pk for tag in new_task.tags.all()],
            form_data["tags"],
        )
        self.assertEqual(
            new_task.deadline,
            form_data["deadline"],
        )

    def test_update_task(self):
        form_data = {
            "content": "TestTask",
            "deadline": timezone.now(),
            "tags": [self.tag.pk],
        }
        self.client.post(reverse("tasks:task-update", args=[1]), data=form_data)
        task = Task.objects.get(pk=1)

        self.assertEqual(task.content, form_data["content"])
        self.assertEqual(task.deadline, form_data["deadline"])
        self.assertEqual(
            [tag.pk for tag in task.tags.all()],
            form_data["tags"],
        )

    def test_delete_task_get_request(self):
        response = self.client.get(
            reverse("tasks:task-delete", args=[1]),
            follow=True,
        )
        self.assertContains(response, "Delete task?")

    def test_delete_task_post_request(self):
        response = self.client.post(
            reverse("tasks:task-delete", args=[1]),
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse("tasks:task-list"),
            status_code=302,
        )
