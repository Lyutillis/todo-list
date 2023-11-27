from django import forms

from tasks.models import Task, Tag


class TaskForm(forms.ModelForm):
    deadline = forms.DateTimeField(
        widget=forms.TextInput(
            attrs={
                "type": "datetime-local",
            }
        ),
        required=False,
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.prefetch_related(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Task
        fields = (
            "deadline",
            "content",
            "tags",
        )
