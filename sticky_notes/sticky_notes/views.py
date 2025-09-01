# sticky_notes/views.py
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render, redirect

from notes.forms import ProfileForm


class PasswordChangeViewWithMessage(PasswordChangeView):
    """
    Password change view that displays a success message upon
    successful password change.

    Fields:
        - form: The password change form.

    Methods:
        - form_valid: Handles a valid form submission with a success
          message.
    """

    template_name = "users/edit_password.html"
    success_url = reverse_lazy("profile")

    def form_valid(self, form):
        """
        :param form: The password change form.
        :return: A redirect response to the success URL.
        """

        response = super().form_valid(form)
        messages.success(
            self.request, "Your password was updated successfully."
        )
        return response


def register(request):
    """
    User registration view.

    :param request: The HTTP request object.
    :return: A rendered registration form or a redirect to the wall.
    """

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            target = (
                request.POST.get("next")
                or request.GET.get("next")
                or "notes:wall"
            )
            return redirect(target)
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})


@login_required(login_url="login")
def view_profile(request):
    """
    View the profile of the logged-in user.

    :param request: The HTTP request object.
    :return: A rendered profile page.
    """

    return render(request, "users/profile.html", {"user": request.user})


@login_required(login_url="login")
def update_details(request):
    """
    Update the details of the logged-in user.

    :param request: The HTTP request object.
    :return: A rendered profile page.
    """

    user = request.user
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile was updated successfully.")
            return redirect("profile")
    else:
        form = ProfileForm(instance=user)
    return render(request, "users/edit_profile.html", {"form": form})
