from django.db import models


class Task(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(blank=True, null=True)
    is_done = models.BooleanField(default=False)
    tags = models.ManyToManyField("Tag", related_name="tasks")

    class Meta:
        ordering = ("is_done", "-created_at")
    
    def __str__(self) -> str:
        return f"{self.content} Done: {self.is_done} Due: {self.deadline}"

    def get_tags(self) -> str|None:
        tags = [tag.name for tag in self.tags.all()]
        if len(tags):
            return ", ".join(tags)


class Tag(models.Model):
    name = models.CharField(max_length=83)

    def __str__(self) -> str:
        return f"Tag: {self.name}"
