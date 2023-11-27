from django.test import TestCase

from tasks.models import Task, Tag


class ModelTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.tag = Tag.objects.create(
            name="TestTag"
        )
        cls.task = Task.objects.create(
            content="TestContent",
        )
        cls.task.tags.set(Tag.objects.filter(pk=1))

    def test_task_str(self):
        self.assertEqual(
            str(self.task),
            f"{self.task.content} Done: {self.task.is_done} Due: {self.task.deadline}",
        )
    
    def test_task_get_tags(self):
        self.assertEqual(
            self.task.get_tags(),
            self.tag.name,
        )

    def test_tag_str(self):
        self.assertEqual(
            str(self.tag),
            f"Tag: {self.tag.name}",
        )
    
