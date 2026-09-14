# 🎭 Theatre API

REST API for managing theatre plays, performances, halls, actors, genres and
tickets. Built with Django REST Framework, JWT authentication and Docker.

## 🌟 Features

- Public catalogue access for plays and performances.
- Staff-only catalogue management.
- JWT authentication and registration.
- Play and performance filtering.
- Ticket purchase with automatic internal reservation creation.
- Seat availability and occupied-place validation.
- Users can view and cancel only their own tickets.
- Swagger UI, ReDoc and API throttling.

## 🛠️ Tech Stack

- Python 3.13
- Django 6.1.1
- Django REST Framework 3.18.1
- Simple JWT
- drf-spectacular
- SQLite
- Docker Compose

## 🚀 Setup

### Local

```bash
python -m venv .venv
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Windows PowerShell activation:

```powershell
.\.venv\Scripts\Activate.ps1
```

API: `http://127.0.0.1:8000/`

### Docker

```bash
docker compose up --build
```

Stop containers:

```bash
docker compose down
```

The project uses SQLite. Migrations run automatically in the container.

## 🔐 Authentication

Register:

```text
POST /api/register/
```

Get tokens:

```text
POST /api/token/
```

Refresh access token:

```text
POST /api/token/refresh/
```

Use the access token:

```text
Authorization: Bearer <access_token>
```

## 🌐 Main Endpoints

### Catalogue

```text
GET    /api/theatre/plays/
POST   /api/theatre/plays/              staff only
GET    /api/theatre/plays/{id}/

GET    /api/theatre/actors/
POST   /api/theatre/actors/              staff only

GET    /api/theatre/genres/
POST   /api/theatre/genres/              staff only

GET    /api/theatre/theatre-halls/
POST   /api/theatre/theatre-halls/       staff only
```

Play filters:

```text
/api/theatre/plays/?title=silent
/api/theatre/plays/?genres=6,13
/api/theatre/plays/?actors=6,7
```

### Performances

```text
GET    /api/theatre/performances/
POST   /api/theatre/performances/        staff only
GET    /api/theatre/performances/{id}/
PUT    /api/theatre/performances/{id}/   staff only
PATCH  /api/theatre/performances/{id}/   staff only
DELETE /api/theatre/performances/{id}/   staff only
```

Filters:

```text
/api/theatre/performances/?play=1,2
/api/theatre/performances/?theatre_hall=1,2
/api/theatre/performances/?date=2026-09-15
```

Performance responses include `tickets_available` and `taken_places`.

### Tickets

Tickets require authentication:

```text
GET    /api/theatre/tickets/
POST   /api/theatre/tickets/
GET    /api/theatre/tickets/{id}/
DELETE /api/theatre/tickets/{id}/
```

Purchase tickets:

```json
{
  "tickets": [
    {"performance": 1, "row": 5, "seat": 12},
    {"performance": 1, "row": 5, "seat": 13}
  ]
}
```

The current user is taken from JWT. Reservation is created internally and is
not a public API resource.

## 📄 Documentation

```text
/api/schema/
/api/schema/swagger-ui/
/api/schema/redoc/
```

## 📦 Fixtures and Admin

Load demo data:

```bash
python manage.py loaddata theatre/fixtures/theatre.json
```

Create an admin user:

```bash
python manage.py createsuperuser
```

Admin panel: `http://127.0.0.1:8000/admin/`

## ⚡ Limits

- Anonymous users: 10 requests per minute.
- Authenticated users: 30 requests per minute.

## ✅ Check

```bash
python manage.py check
```
