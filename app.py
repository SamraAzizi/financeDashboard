
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import sqlite3
from database import initialize_database, add_transaction, get_transactions, get_categories

def main():
    st.set_page_config(page_title="Personal Finance Dashboard", layout="wide")
    st.title("Personal Finance Dashboard")
    
    # Initialize database
    initialize_database()
    
    # Create two columns for layout
    left_col, right_col = st.columns([1, 1])
    
    with left_col:
        create_transaction_form()
        show_transaction_list()
        
    with right_col:
        show_summary()
        show_charts()

def create_transaction_form():
    st.subheader("Add New Transaction")
    
    with st.form("transaction_form", clear_on_submit=True):
        date = st.date_input("Date", value=datetime.now())
        
        # Get categories for the dropdown
        categories = [cat[0] for cat in get_categories()]
        category = st.selectbox("Category", categories)
        
        amount = st.number_input("Amount", min_value=0.0, format="%f")
        description = st.text_input("Description")
        trans_type = st.selectbox("Type", ["income", "expense"])
        
        submitted = st.form_submit_button("Add Transaction")
        
        if submitted:
            try:
                add_transaction(
                    date.strftime('%Y-%m-%d'),
                    category,
                    amount,
                    description,
                    trans_type
                )
                st.success("Transaction added successfully!")
            except Exception as e:
                st.error(f"Error adding transaction: {str(e)}")

def show_transaction_list():
    st.subheader("Recent Transactions")
    
    # Get transactions and convert to DataFrame
    transactions = get_transactions()
    if transactions:
        df = pd.DataFrame(
            transactions,
            columns=['ID', 'Date', 'Category', 'Amount', 'Description', 'Type']
        )
        # Drop the ID column for display
        df = df.drop('ID', axis=1)
        
        # Format the date column
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        
        # Format amount to 2 decimal places
        df['Amount'] = df['Amount'].apply(lambda x: f"${x:,.2f}")
        
        # Display with alternating row colors
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No transactions found")

def show_summary():
    st.subheader("Financial Summary")
    
    transactions = get_transactions()
    if transactions:
        df = pd.DataFrame(
            transactions,
            columns=['ID', 'Date', 'Category', 'Amount', 'Description', 'Type']
        )
        
        total_income = df[df['Type'] == 'income']['Amount'].sum()
        total_expenses = df[df['Type'] == 'expense']['Amount'].sum()
        balance = total_income - total_expenses
        
        # Create three columns for metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Income", f"${total_income:,.2f}")
        with col2:
            st.metric("Total Expenses", f"${total_expenses:,.2f}")
        with col3:
            st.metric("Balance", f"${balance:,.2f}")
    else:
        st.info("No data available for summary")

def show_charts():
    transactions = get_transactions()
    if transactions:
        df = pd.DataFrame(
            transactions,
            columns=['ID', 'Date', 'Category', 'Amount', 'Description', 'Type']
        )
        
        # Convert date strings to datetime
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Expense Distribution Pie Chart
        st.subheader("Expense Distribution")
        expense_by_category = df[df['Type'] == 'expense'].groupby('Category')['Amount'].sum()
        
        fig_pie = px.pie(
            values=expense_by_category.values,
            names=expense_by_category.index,
            title="Expenses by Category"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # Monthly Trend Line Chart
        st.subheader("Monthly Trends")
        monthly_data = df.set_index('Date').resample('M').sum()
        
        fig_line = px.line(
            monthly_data,
            y='Amount',
            title="Monthly Transaction Trends",
            labels={'Amount': 'Total Amount', 'Date': 'Month'}
        )
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("No data available for charts")

if __name__ == "__main__":
    main() 
