# notes/forms.py
from django import forms
from .models import StickyNote
from django.contrib.auth import get_user_model

# Using Django's User so I don't rebuild auth from scratch.
User = get_user_model()


class StickyNoteForm(forms.ModelForm):
    """
    Form for creating and updating StickyNote objects.
    """

    class Meta:
        model = StickyNote
        fields = ["title", "content"]


class ProfileForm(forms.ModelForm):
    """
    Form for updating user profile information.
    """
    
    class Meta:
        model = User
        fields = ["username", "email"]
