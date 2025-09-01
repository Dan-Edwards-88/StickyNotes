# StickyNotes 🗒️

A small Django app for creating, editing and organizing personal sticky notes.  
It shows user authentication, session based access control and simple CRUD for notes. The UI uses Bootstrap with a clean sticky note style.

---

## ✨ Features

- Register, login and logout with Django auth
- Create, view, edit and delete notes
- Wall view that shows a responsive grid of notes, newest first
- Users only see and manage their own notes
- Profile view and edit
- Change password with a success message
- Timestamps shown in the user’s local time with a tiny JS helper

---

## 🧰 Tech stack

- Python and Django
- Bootstrap 5 from CDN plus a little custom CSS
- SQLite by default. You can switch to MariaDB or MySQL
- Vanilla JS for local time formatting

---

## 📁 Project layout

```
sticky_notes/
├─ manage.py
├─ sticky_notes/               # project urls and profile/password views
├─ notes/                      # app: models, views, urls, forms, tests
├─ notes/templates/            # base and app templates
└─ notes/static/notes/         # css, js, images
```

---

## 🚀 Quick start

### 1) Set up the environment

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt    # or: pip install django mysqlclient
```

### 2) Database

The app works with SQLite out of the box.

To use MariaDB or MySQL set this in `settings.py` then run migrations. Django will create the tables for you.

```python
DATABASES = {
  "default": {
    "ENGINE": "django.db.backends.mysql",
    "NAME": "sticky_notes",
    "USER": "appuser",
    "PASSWORD": "yourpassword",
    "HOST": "127.0.0.1",
    "PORT": "3306",
    "OPTIONS": {
      "charset": "utf8mb4",
      "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
    },
    "CONN_MAX_AGE": 60,
  }
}
```

Install the driver if you switch to MariaDB or MySQL:

```bash
pip install mysqlclient
```

### 3) Migrate and run

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/

---

## 🔐 Authentication and URLs

Project urls

- `/login/` uses Django `LoginView` with a custom template
- `/logout/` uses Django `LogoutView`
- `/password/change/` uses a custom view that redirects to Profile with a success message
- `/account/` shows the Profile page
- `/account/edit/` lets you edit profile data

Notes app urls (namespace `notes:`)

- `notes:wall` shows the note wall
- `notes:create` creates a new note
- `notes:detail` shows a single note
- `notes:edit` edits a note
- `notes:delete` deletes a note with POST

Templates call urls by name. For example `{% url 'notes:wall' %}`. This keeps templates stable if mount points change.

---

## 🧪 Tests

A simple suite lives in `notes/tests.py`.

- Model: `__str__` and ownership
- Form: required fields
- Views: wall requires login and CRUD for the owner and ownership guard for non owners

Run tests:

```bash
python manage.py test notes
```

You should see `OK` when they pass.

---

## 🎨 Front end notes

- Local time helper lives in `notes/static/notes/js/localtime.js`. Any `<time class="js-localtime" datetime="...">` is converted on the client
- Sticky look comes from `notes/static/notes/css/app.css`. Notes have a paper style with a small pin and a soft shadow

---

## 🧭 Developer notes

- Session cookies should be `Secure`, `HttpOnly` and set a suitable `SameSite`
- Rotate the session id on login to avoid fixation
- Notes are ordered newest first with model `Meta.ordering` or `.order_by('-updated_at')`
- Every note query filters by `user=request.user` so guessing ids returns a 404 for non owners
- Static analyzers may not see `user.notes` since Django creates it at runtime. You can query `StickyNote.objects.filter(user=user)` or add a small ignore comment

---

## 🛠️ Useful commands

```bash
# Create migrations after model changes then apply
python manage.py makemigrations
python manage.py migrate

# Collect static files for deployment
python manage.py collectstatic
```

---

## 📄 License

```
MIT License

Copyright (c) 2025 Dan Edwards

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Author

Dan Edwards - Assignment submission for **M06T05 - Sticky Notes Application**
