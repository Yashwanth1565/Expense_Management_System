from sqlalchemy.orm import Session
import models

# Create
def create_expense(db: Session, expense):
    db_expense = models.Expense(
        employee_name=expense.employee_name,
        amount=expense.amount,
        category=expense.category,
        description=expense.description
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


# Read with filters
def get_expenses(db: Session, name=None, status=None):
    query = db.query(models.Expense)

    if name:
        query = query.filter(models.Expense.employee_name.ilike(f"%{name}%"))

    if status:
        query = query.filter(models.Expense.status == status)

    return query.all()


# Update
def update_expense(db: Session, expense_id: int, updated_data):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()

    if not expense:
        return None

    if expense.status != "Pending":
        return "NOT_ALLOWED"

    expense.employee_name = updated_data.employee_name
    expense.amount = updated_data.amount
    expense.category = updated_data.category
    expense.description = updated_data.description

    db.commit()
    db.refresh(expense)
    return expense


# Delete
def delete_expense(db: Session, expense_id: int):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()

    if not expense:
        return None

    if expense.status != "Pending":
        return "NOT_ALLOWED"

    db.delete(expense)
    db.commit()
    return True


# Approve / Reject
def update_status(db: Session, expense_id: int, status: str):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()

    if not expense:
        return None

    if expense.status != "Pending":
        return "NOT_ALLOWED"

    expense.status = status
    db.commit()
    db.refresh(expense)
    return expense


# Dashboard
def get_dashboard(db: Session):
    total = db.query(models.Expense).count()
    approved = db.query(models.Expense).filter(models.Expense.status == "Approved").count()
    rejected = db.query(models.Expense).filter(models.Expense.status == "Rejected").count()

    return {
        "total": total,
        "approved": approved,
        "rejected": rejected
    }