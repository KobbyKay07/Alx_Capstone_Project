# Task Management API

A simple Task Management API built with **Django** and **Django REST Framework (DRF)**.  
This project allows users to create, view, update, and delete tasks, with each task linked to a user.

---

## Features
- User management (using Django’s built‑in `User` model).
- Task CRUD operations:
  - Create a task
  - Retrieve all tasks or a single task
  - Update a task
  - Delete a task
- Each task is associated with a user.
- JSON responses for easy integration with frontend or mobile apps.

---

## Project Structure
Alx_Capstone_Project/
├── tasks/ # App containing models, views, serializers, urls 
│ ├── models.py 
│ ├── serializers.py 
│ ├── views.py 
│ ├── urls.py 
├── Task_Management/ # Project settings 
│ ├── settings.py 
│ ├── urls.py 
├── manage.py



## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/KobbyKay07/Alx_Capstone_Project.git
   cd Alx_Capstone_Project

2. **Install Django**
   ```bash
   pip install django
   pip install djangorestframework

3. **Start Project**
   ```bash
   django-admin startproject Task_Management

4. **Add App**
   ```bash
   python manage.py startapp Task

5. **Apply Migrations**
   ```bash
   python manage.py migrate

6. **Run The Server**
   ```bash
   python manage.py runserver



**API Endpoints**
Tasks
POST /api/tasks/ → Create a new task Example payload:

json
{
  "title": "Buy groceries",
  "description": "Milk, bread, eggs",
  "user": 1
}
GET /api/tasks/ → Retrieve all tasks

GET /api/tasks/<id>/ → Retrieve a single task

PUT /api/tasks/<id>/ → Update a task Example payload:

json
{
  "title": "Buy groceries",
  "description": "Milk, bread, eggs, butter",
  "is_completed": true
}
DELETE /api/tasks/<id>/ → Delete a task