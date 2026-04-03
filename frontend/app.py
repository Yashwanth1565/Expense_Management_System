import streamlit as st
import pandas as pd

from database import SessionLocal, engine
import models, crud

# Create tables
models.Base.metadata.create_all(bind=engine)

# ---------------- UI Styling ----------------
st.set_page_config(page_title="Expense System", layout="wide")

st.markdown("""
<style>
.stApp {
    background-image: url("https://images.unsplash.com/photo-1519389950473-47ba0277781c");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

.main {
    background-color: rgba(0, 0, 0, 0.7);
    padding: 20px;
    border-radius: 15px;
}

section[data-testid="stSidebar"] {
    background: rgba(0, 0, 0, 0.9);
}

.stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 10px;
    height: 45px;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;color:white;'>Expense Approval System</h1>", unsafe_allow_html=True)

menu = st.sidebar.selectbox("Menu", [
    "Dashboard",
    "Submit Expense",
    "View Expenses",
    "Update Expense",
    "Delete Expense",
    "Approve/Reject"
])

db = SessionLocal()

# ---------------- Dashboard ----------------
if menu == "Dashboard":
    data = crud.get_dashboard(db)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total", data["total"])
    col2.metric("Approved", data["approved"])
    col3.metric("Rejected", data["rejected"])


# ---------------- Submit ----------------
elif menu == "Submit Expense":
    name = st.text_input("Employee Name")
    amount = st.number_input("Amount", min_value=1)
    category = st.text_input("Category")
    description = st.text_input("Description")

    if st.button("Submit"):
        crud.create_expense(db, type("obj", (), {
            "employee_name": name,
            "amount": amount,
            "category": category,
            "description": description
        }))
        st.success("✅ Submitted Successfully")


# ---------------- View ----------------
elif menu == "View Expenses":
    name_filter = st.text_input("Search Name")
    status_filter = st.selectbox("Status", ["", "Pending", "Approved", "Rejected"])

    data = crud.get_expenses(db, name_filter, status_filter)

    if data:
        df = pd.DataFrame([{
            "ID": e.id,
            "Name": e.employee_name,
            "Amount": e.amount,
            "Category": e.category,
            "Description": e.description,
            "Date": e.date,
            "Status": e.status
        } for e in data])

        st.dataframe(df)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", csv, "expenses.csv", "text/csv")
    else:
        st.warning("No data found")


# ---------------- Update ----------------
elif menu == "Update Expense":
    id = st.number_input("Expense ID", step=1)
    name = st.text_input("Name")
    amount = st.number_input("Amount", min_value=1)
    category = st.text_input("Category")
    description = st.text_input("Description")

    if st.button("Update"):
        result = crud.update_expense(db, id, type("obj", (), {
            "employee_name": name,
            "amount": amount,
            "category": category,
            "description": description
        }))

        if result == "NOT_ALLOWED":
            st.error("Only Pending can be updated")
        elif result is None:
            st.error("Not found")
        else:
            st.success("Updated Successfully")


# ---------------- Delete ----------------
elif menu == "Delete Expense":
    id = st.number_input("Expense ID", step=1)

    if st.button("Delete"):
        result = crud.delete_expense(db, id)

        if result == "NOT_ALLOWED":
            st.error("Only Pending can be deleted")
        elif result is None:
            st.error("Not found")
        else:
            st.success("Deleted Successfully")


# ---------------- Approve ----------------
elif menu == "Approve/Reject":
    id = st.number_input("Expense ID", step=1)
    status = st.selectbox("Status", ["Approved", "Rejected"])

    if st.button("Submit"):
        result = crud.update_status(db, id, status)

        if result == "NOT_ALLOWED":
            st.error("Already processed")
        elif result is None:
            st.error("Not found")
        else:
            st.success(f"{status} Successfully")
