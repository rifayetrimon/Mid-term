from fastapi import FastAPI

from app.db.database import Base, engine
from app.models import Transaction, User
from app.routers import transactions, users

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Expense Tracker API")

app.include_router(users.router)
app.include_router(transactions.router)


@app.get("/")
def home():
    return {"message": "Expense Tracker API is running"}
