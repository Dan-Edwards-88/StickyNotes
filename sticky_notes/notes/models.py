# notes/models.py
from django.db import models
from django.conf import settings


class StickyNote(models.Model):
    """
    Model representing a sticky note owned by an auth'd user.

    Fields:
        - note_id: IntegerField for the note's ID. (unique PK)
        - title: CharField for the note's title.
        - content: TextField for the note's content.
        - created_at: DateTimeField for when the note was created.
        - updated_at: DateTimeField for when the note was last updated.
        - user: ForeignKey to the User model, representing the note's 
          owner.

    Methods:
        - Meta: Defines ordering and indexes.
        - __str__: Returns a string representation of the note,
          showing the title.

    :param models.Model: Django's base model class.
    """

    note_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notes",
    )

    class Meta:
        ordering = ("-updated_at",)
        indexes = [models.Index(fields=["user", "-updated_at"])]

    def __str__(self):
        return self.title
