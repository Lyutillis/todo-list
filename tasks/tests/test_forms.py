from django.utils import timezone
from django.test import TestCase

from tasks.models import Tag, Task
from tasks.forms import TaskForm


class TestForms(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        tag = Tag.objects.create(
            name="TestTag"
        )

    def test_task_form(self):
        form_data = {
            "deadline": timezone.now(),
            "content": "TestContent",
            "tags": Tag.objects.filter(pk=1)
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["deadline"], form_data["deadline"])
        self.assertEqual(
            form.cleaned_data["content"],
            form_data["content"],
        )
        self.assertEqual(
            list(form.cleaned_data["tags"]),
            list(form_data["tags"]),
        )
