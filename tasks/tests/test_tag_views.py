from django.test import TestCase
from django.urls import reverse

from tasks.models import Tag

TAGS_URL = reverse("tasks:tag-list")


class PublicTagTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_tags = 23

        for tag_id in range(number_of_tags):
            Tag.objects.create(
                name=f"Tag {tag_id}",
            )

    def test_retrieve_tags(self):
        response = self.client.get(TAGS_URL)
        self.assertEqual(response.status_code, 200)
        tags = Tag.objects.all()
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["tag_list"]), 4)
        self.assertEqual(list(response.context["tag_list"]), list(tags)[:4])
        self.assertTemplateUsed(response, "tasks/tag_list.html")

    def test_retrieve_tags_last_page(self):
        response = self.client.get(TAGS_URL + "?page=6")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["tag_list"]), 3)

    def test_create_tag(self):
        form_data = {
            "name": "TestTag",
        }
        self.client.post(reverse("tasks:tag-create"), data=form_data)

        new_tag = Tag.objects.filter(name=form_data["name"]).first()

        self.assertIsNotNone(new_tag)

    def test_update_tag(self):
        form_data = {
            "name": "NotTestTag",
        }
        self.client.post(reverse("tasks:tag-update", args=[1]), data=form_data)
        tag = Tag.objects.get(pk=1)

        self.assertEqual(tag.name, form_data["name"])

    def test_delete_tag_get_request(self):
        response = self.client.get(
            reverse("tasks:tag-delete", args=[1]),
            follow=True,
        )
        self.assertContains(response, "Delete tag?")

    def test_delete_tag_post_request(self):
        response = self.client.post(
            reverse("tasks:tag-delete", args=[1]),
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse("tasks:tag-list"),
            status_code=302,
        )
