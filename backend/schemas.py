from pydantic import BaseModel, Field

class ExpenseCreate(BaseModel):
    employee_name: str
    amount: int = Field(gt=0)
    category: str
    description: str


class ExpenseUpdate(BaseModel):
    employee_name: str
    amount: int = Field(gt=0)
    category: str
    description: str


class ExpenseStatusUpdate(BaseModel):
    status: str