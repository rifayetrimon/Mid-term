from datetime import date

from pydantic import BaseModel, ConfigDict, field_validator


class TransactionCreate(BaseModel):
    title: str
    amount: float
    type: str
    category: str
    date: date

    @field_validator("amount")
    def check_amount(cls, value):
        if value <= 0:
            raise ValueError("amount must be a positive number")
        return value

    @field_validator("type")
    def check_type(cls, value):
        if value not in ["income", "expense"]:
            raise ValueError("type must be income or expense")
        return value


class TransactionOut(BaseModel):
    id: int
    title: str
    amount: float
    type: str
    category: str
    date: date
    owner_id: int

    model_config = ConfigDict(from_attributes=True)
