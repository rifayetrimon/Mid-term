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

## Environment Variables

| Name | Default | Description |
| --- | --- | --- |
| DATABASE_URL | sqlite:///./expense.db | Database connection string |
| SECRET_KEY | (local dev value) | Key used to sign the JWT token |

## Deploy on Render

1. Push the project to GitHub.
2. On Render click **New** and choose **Web Service**, then connect this repository.
3. Fill the settings:
   - Runtime: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add an environment variable `SECRET_KEY` with any long random value.
5. Click **Create Web Service** and wait for the build to finish.

The repo also has a `render.yaml`, so **New > Blueprint** can be used instead
and Render will read all the settings from that file.

Live docs after deploy: `https://<service-name>.onrender.com/docs`

Note: the free Render disk is temporary. The SQLite file is created again on
every deploy or restart, so old users and transactions are cleared. To keep the
data, create a Render PostgreSQL database and set its connection string as the
`DATABASE_URL` environment variable (also add `psycopg2-binary` to
requirements.txt). No code change is needed.
