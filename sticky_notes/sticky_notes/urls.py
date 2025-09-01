# sticky_notes/urls.py
from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views
from .views import PasswordChangeViewWithMessage

urlpatterns = [
    path("", include(("notes.urls", "notes"), namespace="notes")),
    path("register/", views.register, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html",
            redirect_authenticated_user=True
        ),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="login"),
        name="logout",
    ),
    path(
        "password/change/",
        PasswordChangeViewWithMessage.as_view(),
        name="password_change",
    ),
    path("account/", views.view_profile, name="profile"),
    path("account/edit/", views.update_details, name="profile_edit"),
]
