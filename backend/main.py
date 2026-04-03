from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

import models, schemas, crud
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# DB connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create Expense
@app.post("/expenses/")
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    return crud.create_expense(db, expense)


# Get Expenses with filters
@app.get("/expenses/")
def get_expenses(
    employee_name: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return crud.get_expenses(db, employee_name, status)


# Update Expense
@app.put("/expenses/{expense_id}")
def update_expense(expense_id: int, data: schemas.ExpenseUpdate, db: Session = Depends(get_db)):
    result = crud.update_expense(db, expense_id, data)

    if result is None:
        raise HTTPException(status_code=404, detail="Expense not found")

    if result == "NOT_ALLOWED":
        raise HTTPException(status_code=400, detail="Only Pending expenses can be updated")

    return result


# Delete Expense
@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    result = crud.delete_expense(db, expense_id)

    if result is None:
        raise HTTPException(status_code=404, detail="Expense not found")

    if result == "NOT_ALLOWED":
        raise HTTPException(status_code=400, detail="Only Pending expenses can be deleted")

    return {"message": "Deleted successfully"}


# Approve / Reject
@app.put("/expenses/{expense_id}/status")
def update_status(expense_id: int, data: schemas.ExpenseStatusUpdate, db: Session = Depends(get_db)):

    if data.status not in ["Approved", "Rejected"]:
        raise HTTPException(status_code=400, detail="Invalid status")

    result = crud.update_status(db, expense_id, data.status)

    if result is None:
        raise HTTPException(status_code=404, detail="Expense not found")

    if result == "NOT_ALLOWED":
        raise HTTPException(status_code=400, detail="Already processed")

    return result


# Dashboard
@app.get("/dashboard/")
def dashboard(db: Session = Depends(get_db)):
    return crud.get_dashboard(db)