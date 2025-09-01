# notes/tests.py
# Use case tests for the StickyNotes app.

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import StickyNote
from .forms import StickyNoteForm

User = get_user_model()

# Test to ensure StickyNote model's string representation is correct
class StickyNoteModelTests(TestCase):
    def test_str_returns_title(self):
        user = User.objects.create_user(username="alice", password="pass12345")
        note = StickyNote.objects.create(user=user, title="Grocery list", content="Milk")
        self.assertEqual(str(note), "Grocery list")


# Test to ensure forms are working correctly
class StickyNoteFormTests(TestCase):
    def test_form_valid_with_title_and_content(self):
        form = StickyNoteForm(data={"title": "OK", "content": "Some text"})
        self.assertTrue(form.is_valid())

    def test_form_invalid_when_missing_fields(self):
        form = StickyNoteForm(data={"title": "", "content": ""})
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)
        self.assertIn("content", form.errors)


# Test to ensure notes cant be posted without logging in
class WallViewAuthTests(TestCase):
    def test_wall_requires_login(self):
        resp = self.client.get(reverse("notes:wall"))
        self.assertEqual(resp.status_code, 302)
        self.assertIn("next=", resp["Location"])


class NoteViewsBasicFlowTests(TestCase):
    """
    These tests cover the happy-path CRUD for the note owner.
    Keep it simple: log a user in, create a note, view it, edit it, delete it.
    """

    # Set up test users and notes
    def setUp(self):
        self.user = User.objects.create_user(username="bob", password="pass12345")
        self.client.login(username="bob", password="pass12345")

    # Test the full CRUD lifecycle for a note
    def test_create_note(self):
        url = reverse("notes:create")
        resp = self.client.post(url, {"title": "T", "content": "C"})
        self.assertEqual(resp.status_code, 302) 
        self.assertEqual(self.user.notes.count(), 1) # type: ignore
        note = self.user.notes.first() # type: ignore
        self.assertEqual(note.title, "T")
        self.assertEqual(note.content, "C")

    # Test viewing own note detail
    def test_view_own_note_detail(self):
        note = StickyNote.objects.create(user=self.user, title="Hello", content="World")
        url = reverse("notes:detail", kwargs={"note_id": note.pk})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Hello")

    # Test editing own note
    def test_edit_own_note(self):
        note = StickyNote.objects.create(user=self.user, title="Old", content="Body")
        url = reverse("notes:edit", kwargs={"note_id": note.pk})
        resp = self.client.post(url, {"title": "New", "content": "Body2"})
        self.assertEqual(resp.status_code, 302)
        note.refresh_from_db()
        self.assertEqual(note.title, "New")
        self.assertEqual(note.content, "Body2")

    # Test deleting own note
    def test_delete_own_note(self):
        note = StickyNote.objects.create(user=self.user, title="Soon gone", content="Bye")
        url = reverse("notes:delete", kwargs={"note_id": note.pk})
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(StickyNote.objects.filter(pk=note.pk).exists())


class NoteOwnershipGuardTests(TestCase):
    """
    Make sure users can't view/edit/delete someone else's note.
    """

    # Set up test users and notes
    def setUp(self):
        self.owner = User.objects.create_user(username="owner", password="pass12345")
        self.intruder = User.objects.create_user(username="eve", password="pass12345")
        self.note = StickyNote.objects.create(user=self.owner, title="Private", content="Top secret")

    # Test non-owner cannot view detail
    def test_non_owner_cannot_view_detail(self):
        self.client.login(username="eve", password="pass12345")
        url = reverse("notes:detail", kwargs={"note_id": self.note.pk})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)
