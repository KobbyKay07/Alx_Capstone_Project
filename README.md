📘 Task Management API
📌 Overview
The Task Management API is a backend system built with Django and Django REST Framework (DRF). It provides secure authentication, task workflows, and user management features, designed for scalability and collaboration.

🚀 Features
🔐 JWT Authentication

Login with username & password.

Access and refresh tokens for secure session management.

👥 Custom User Model

Flexible user accounts.

Supports superuser and staff roles.

📋 Task Management (CRUD)

Create, read, update, and delete tasks.

Task status workflow: pending, in‑progress, completed.

🔄 Recurring Tasks & Notifications

Signal‑based architecture for automated updates.

Prevents duplicate task creation.

🛡️ Permissions & Ownership

Only task owners can edit or delete tasks.

Anonymous users blocked (401 Unauthorized).

🔎 Filtering & Query Parameters

Filter tasks by status or other fields using django-filter.

⚡ Deployment Ready

requirements.txt for reproducible installs.

Whitenoise for static file handling.

Configured for PythonAnywhere deployment.

🛠️ Tech Stack
Backend: Django, Django REST Framework

Auth: djangorestframework-simplejwt

Filtering: django-filter

Environment Management: django-environ

Static Files: Whitenoise

Deployment: PythonAnywhere

📂 Project Structure
Code
Alx_Capstone_Project/
│── requirements.txt
│── Task_Management/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── permissions.py
│   └── ...
🧪 API Endpoints
Auth
POST /api/token/ → Get access & refresh tokens.

POST /api/token/refresh/ → Refresh access token.

Tasks
GET /api/tasks/ → List tasks.

POST /api/tasks/ → Create task.

PUT /api/tasks/<id>/ → Update task.

DELETE /api/tasks/<id>/ → Delete task.

📝 Usage Instructions
Run locally:

bash
python manage.py runserver
Open Postman:

POST /api/token/ → login with credentials.

Use Authorization: Bearer <access_token> header.

Test CRUD endpoints.

Access Django Admin:

Code
http://127.0.0.1:8000/admin/
