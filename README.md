# Expense Tracker API

FastAPI project with JWT authentication, SQLAlchemy ORM and SQLite database.

## Folder Structure

```
.
├── app/
│   ├── core/
│   │   ├── config.py          settings (database url, jwt config)
│   │   └── security.py        password hashing and jwt token
│   ├── db/
│   │   └── database.py        engine, session, base, get_db
│   ├── models/
│   │   ├── user.py            User table
│   │   └── transaction.py     Transaction table
│   ├── schemas/
│   │   ├── user.py            user pydantic models
│   │   └── transaction.py     transaction pydantic models
│   ├── routers/
│   │   ├── users.py           /auth routes
│   │   └── transactions.py    /transactions routes
│   ├── dependencies.py        get_current_user
│   └── main.py                app object
├── tests/
│   ├── conftest.py            test database and fixtures
│   ├── test_auth.py
│   └── test_transactions.py
├── requirements.txt
└── README.md
```

## Setup

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Docs: http://127.0.0.1:8000/docs

## Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | /auth/register | Create a new user |
| POST | /auth/login | Login and get JWT token |
| POST | /transactions | Create a transaction |
| GET | /transactions | Get all transactions of the logged in user |
| GET | /transactions/filter | Filter transactions |
| GET | /transactions/{id} | Get one transaction |
| PUT | /transactions/{id} | Update a transaction |
| DELETE | /transactions/{id} | Delete a transaction |

All transaction routes need the header `Authorization: Bearer <token>`.

## Filter example

```
/transactions/filter?type=expense&category=Food&minimum_amount=100&maximum_amount=5000
```

## Run tests

```
pytest
```
