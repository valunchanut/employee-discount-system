
import streamlit as st

# Initialize state
if "employees" not in st.session_state:
    st.session_state.employees = []

# Utility functions
def check_employee_exists(emp_id):
    return any(emp[0] == emp_id for emp in st.session_state.employees)

def check_employee_discount_exists(discount_id):
    return any(emp[6] == discount_id for emp in st.session_state.employees)

def find_employee_discount(discount_id):
    for i, emp in enumerate(st.session_state.employees):
        if emp[6] == discount_id:
            return i
    return -1

# Main UI
st.title("Employee Discount System")

menu = st.sidebar.radio("Menu", ["Add Employee", "Add Purchase", "View Employees", "Search by Discount ID"])

# Add Employee Form
if menu == "Add Employee":
    st.header("Add New Employee")
    with st.form("employee_form"):
        emp_id = st.number_input("Employee ID", min_value=1, step=1)
        name = st.text_input("Name")
        emp_type = st.selectbox("Type", ["hourly", "manager"])
        years = st.number_input("Years Worked", min_value=0)
        discount_id = st.number_input("Discount ID", min_value=1, step=1)
        submitted = st.form_submit_button("Add Employee")

        if submitted:
            if name.strip() == "":
                st.warning("Name cannot be empty.")
            elif check_employee_exists(emp_id):
                st.warning("Employee ID already exists.")
            elif check_employee_discount_exists(discount_id):
                st.warning("Discount ID already exists.")
            else:
                st.session_state.employees.append([emp_id, name, emp_type, years, 0.0, 0.0, discount_id])
                st.success(f"Employee {name} added.")

# Add Purchase
elif menu == "Add Purchase":
    st.header("Add Purchase")
    discount_id = st.number_input("Discount ID", min_value=1, step=1)
    amount = st.number_input("Purchase Amount", min_value=0.0, step=0.01)
    if st.button("Submit Purchase"):
        index = find_employee_discount(discount_id)
        if index == -1:
            st.error("Discount ID not found.")
        else:
            emp = st.session_state.employees[index]
            emp[4] += amount
            if emp[2] == "hourly":
                discount = amount * 0.1 + (emp[3] * 0.01 * amount)
            else:
                discount = amount * 0.15 + (emp[3] * 0.02 * amount)
            emp[5] += discount
            st.success(f"Purchase of {amount} added. Discount: {discount:.2f}")

# View all employees
elif menu == "View Employees":
    st.header("All Employees")
    if st.session_state.employees:
        st.dataframe(st.session_state.employees, use_container_width=True)
    else:
        st.info("No employees yet.")

# Search by Discount ID
elif menu == "Search by Discount ID":
    st.header("Search Employee by Discount ID")
    search_id = st.number_input("Enter Discount ID", min_value=1, step=1)
    if st.button("Search"):
        idx = find_employee_discount(search_id)
        if idx == -1:
            st.error("No employee found with that Discount ID.")
        else:
            emp = st.session_state.employees[idx]
            st.write(f"ID: {emp[0]}, Name: {emp[1]}, Type: {emp[2]}")
            st.write(f"Years Worked: {emp[3]}, Total Purchased: {emp[4]}, Total Discount: {emp[5]}")
