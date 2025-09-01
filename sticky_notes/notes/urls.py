# notes/urls.py
from django.urls import path
from .views import (
    sticky_note_wall,
    view_sticky_note,
    add_sticky_note,
    edit_sticky_note,
    delete_sticky_note,
)

app_name = "notes"

urlpatterns = [
    # /notes/
    path("", sticky_note_wall, name="wall"),

    # /notes/new/
    path("new/", add_sticky_note, name="create"),

    # /notes/<int:note_id>/
    path("<int:note_id>/", view_sticky_note, name="detail"),

    # /notes/<int:note_id>/edit/
    path("<int:note_id>/edit/", edit_sticky_note, name="edit"),

    # /notes/<int:note_id>/delete/
    path("<int:note_id>/delete/", delete_sticky_note, name="delete"),
]
