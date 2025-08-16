# Library Service Project

## Project Overview
**Library-Service-Project** is a backend application designed to automate library management processes: managing books, users, borrowings, and returns.  
It provides a modern REST API to replace outdated manual systems.

## Project Structure
- `library/books/` — app for managing books (CRUD, search, filtering).
- `borrowings/` — app for borrow/return operations, due dates, fines.
- `user/` — registration, authentication.
- `doc/swagger/` — documentation

## Installation & Setup

### Requirements
- Python 3.10+
- pip & virtualenv

### Setup Steps
```bash
git clone https://github.com/Andreyome/Library-Service-Project.git
cd Library-Service-Project
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```
### Environment Configuration 
Copy .env.example → .env and set values:

DB_NAME, DB_USER, DB_PASSWORD, SECRET_KEY etc.

Run migrations:
`python manage.py migrate`

Run the server
`python manage.py runserver`

### ENDPOINTS

| Endpoint                       | Method   | Description                              |
|--------------------------------|----------|------------------------------------------|
| `/api/library/books/`          | GET      | List all books                           |
| `/api/library/books/`          | POST     | Add a new book                           |
| `/api/library/books/{id}/`     | GET      | Get book details by ID                   |
| `/api/library/books/{id}/`     | PUT      | Update book details (full)               |
| `/api/library/books/{id}/`     | PATCH    | Update book details (partial)            |
| `/api/library/books/{id}/`     | DELETE   | Delete a book                            |
| `/api/borrowings/`             | GET      | List all borrow/return operations        |
| `/api/borrowings/{id}/`        | GET      | Get detail borrowing by id               |
| `/api/borrowings/`             | POST     | Create a new borrowing operation         |
| `/api/borrowings/{id}/return/` | POST     | Return a borrowed book by operation ID   |
| `/api/users/`                  | GET/POST | User registration & list users           |
| `/api/auth/`                   | POST     | User authentication (JWT, session, etc.) |

### DOCKER
1. Build and start the containers

`docker-compose up --build`

2. Access the application

Django app: http://localhost:8000
