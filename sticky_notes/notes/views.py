from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views.decorators.http import require_POST

from .models import StickyNote
from .forms import StickyNoteForm

User = get_user_model()


@login_required(login_url="login")
def sticky_note_wall(request):
    """
    Show the user's sticky notes.

    :param request: The HTTP request object.
    :return: A rendered template with the user's sticky notes.
    """

    # Only show this user's notes
    notes = StickyNote.objects.filter(user=request.user)
    return render(request, "notes/wall.html", {"notes": notes})


@login_required(login_url="login")
def view_sticky_note(request, note_id):
    """
    View a single sticky note.

    :param request: The HTTP request object.
    :param note_id: The ID of the sticky note to view.
    :return: A rendered template with the sticky note details.
    """

    note = get_object_or_404(StickyNote, pk=note_id, user=request.user)
    return render(request, "notes/note.html", {"note": note})


@login_required(login_url="login")
def add_sticky_note(request):
    """
    Add a new sticky note.

    :param request: The HTTP request object.
    :return: A rendered template with the sticky note form.
    """

    if request.method == "POST":
        form = StickyNoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(request, "Note created.")
            return redirect("notes:wall")
    else:
        form = StickyNoteForm()
    return render(request, "notes/add_note.html", {"form": form})


@login_required(login_url="login")
def edit_sticky_note(request, note_id):
    """
    Edit an existing sticky note.

    :param request: The HTTP request object.
    :param note_id: The ID of the sticky note to edit.
    :return: A rendered template with the sticky note form.
    """

    note = get_object_or_404(StickyNote, pk=note_id, user=request.user)
    if request.method == "POST":
        form = StickyNoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, "Note updated.")
            return redirect("notes:detail", note_id=note.pk)
    else:
        form = StickyNoteForm(instance=note)
    return render(
        request, "notes/edit_note.html", {"form": form, "note": note}
    )


@require_POST
@login_required(login_url="login")
def delete_sticky_note(request, note_id):
    """
    Delete an existing sticky note.

    :param request: The HTTP request object.
    :param note_id: The ID of the sticky note to delete.
    :return: A redirect to the sticky note wall.
    """

    note = get_object_or_404(StickyNote, pk=note_id, user=request.user)
    note.delete()
    messages.success(request, "Note deleted.")
    return redirect("notes:wall")
