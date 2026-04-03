import streamlit as st
import requests
import pandas as pd

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Expense System", layout="wide")

st.title(" Expense Approval System")
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1557683316-973673baf926");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Make content semi-transparent */
    .main {
        background-color: rgba(0, 0, 0, 0.7);
        padding: 20px;
        border-radius: 15px;
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: rgba(0, 0, 0, 0.9);
    }

    /* Input fields */
    input, textarea {
        background-color: #1e1e1e !important;
        color: white !important;
        border-radius: 8px !important;
    }

    /* Buttons */
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        height: 45px;
        width: 100%;
        font-size: 16px;
    }

    </style>
""", unsafe_allow_html=True)

menu = st.sidebar.selectbox("Menu", [
    "Dashboard",
    "Submit Expense",
    "View Expenses",
    "Update Expense",
    "Delete Expense",
    "Approve/Reject"
])


# Dashboard
if menu == "Dashboard":
    res = requests.get(f"{BASE_URL}/dashboard/")
    data = res.json()

    st.subheader("📊 Dashboard")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total", data["total"])
    col2.metric("Approved", data["approved"])
    col3.metric("Rejected", data["rejected"])


# Submit
elif menu == "Submit Expense":
    name = st.text_input("Employee Name")
    amount = st.number_input("Amount", min_value=1)
    category = st.text_input("Category")
    description = st.text_input("Description")

    if st.button("Submit"):
        res = requests.post(f"{BASE_URL}/expenses/", json={
            "employee_name": name,
            "amount": amount,
            "category": category,
            "description": description
        })

        if res.status_code == 200:
            st.success("✅ Expense Submitted Successfully")
        else:
            st.error("❌ Error submitting expense")


# View
elif menu == "View Expenses":

    st.subheader("🔍 Filter Expenses")

    name_filter = st.text_input("Search by Employee Name")
    status_filter = st.selectbox("Status", ["", "Pending", "Approved", "Rejected"])

    params = {}
    if name_filter:
        params["employee_name"] = name_filter
    if status_filter:
        params["status"] = status_filter

    res = requests.get(f"{BASE_URL}/expenses/", params=params)
    data = res.json()

    if data:
        df = pd.DataFrame(data)
        st.dataframe(df)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", csv, "expenses.csv", "text/csv")
    else:
        st.warning("No data found")


# Update
elif menu == "Update Expense":
    id = st.number_input("Expense ID", step=1)
    name = st.text_input("Employee Name")
    amount = st.number_input("Amount", min_value=1)
    category = st.text_input("Category")
    description = st.text_input("Description")

    if st.button("Update"):
        res = requests.put(f"{BASE_URL}/expenses/{id}", json={
            "employee_name": name,
            "amount": amount,
            "category": category,
            "description": description
        })

        if res.status_code == 200:
            st.success("✅ Updated Successfully")
        else:
            st.error(res.json()["detail"])


# Delete
elif menu == "Delete Expense":
    id = st.number_input("Expense ID", step=1)

    if st.button("Delete"):
        res = requests.delete(f"{BASE_URL}/expenses/{id}")

        if res.status_code == 200:
            st.success("✅ Deleted Successfully")
        else:
            st.error(res.json()["detail"])


# Approve / Reject
elif menu == "Approve/Reject":
    id = st.number_input("Expense ID", step=1)
    status = st.selectbox("Status", ["Approved", "Rejected"])

    if st.button("Submit"):
        res = requests.put(f"{BASE_URL}/expenses/{id}/status", json={
            "status": status
        })

        if res.status_code == 200:
            st.success(f"✅ Expense {status}")
        else:
            st.error(res.json()["detail"])