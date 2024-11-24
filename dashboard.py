import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from database import add_transaction, get_transactions, get_categories

class Dashboard:
    def __init__(self, parent):
        self.parent = parent
        
        # Create main frames
        self.create_frames()
        self.create_transaction_form()
        self.create_summary()
        self.create_transaction_list()
        
    def create_frames(self):
        # Left frame for form and transactions
        self.left_frame = ttk.Frame(self.parent)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Right frame for summary and charts
        self.right_frame = ttk.Frame(self.parent)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
    def create_transaction_form(self):
        # Transaction form frame
        form_frame = ttk.LabelFrame(self.left_frame, text="Add Transaction")
        form_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Date
        ttk.Label(form_frame, text="Date:").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = ttk.Entry(form_frame)
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Category
        ttk.Label(form_frame, text="Category:").grid(row=1, column=0, padx=5, pady=5)
        self.category_combobox = ttk.Combobox(form_frame, values=[cat[0] for cat in get_categories()])
        self.category_combobox.grid(row=1, column=1, padx=5, pady=5)
        
        # Amount
        ttk.Label(form_frame, text="Amount:").grid(row=2, column=0, padx=5, pady=5)
        self.amount_entry = ttk.Entry(form_frame)
        self.amount_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Description
        ttk.Label(form_frame, text="Description:").grid(row=3, column=0, padx=5, pady=5)
        self.description_entry = ttk.Entry(form_frame)
        self.description_entry.grid(row=3, column=1, padx=5, pady=5)
        
        # Type
        ttk.Label(form_frame, text="Type:").grid(row=4, column=0, padx=5, pady=5)
        self.type_combobox = ttk.Combobox(form_frame, values=['income', 'expense'])
        self.type_combobox.grid(row=4, column=1, padx=5, pady=5)
        
        # Submit button
        submit_btn = ttk.Button(form_frame, text="Add Transaction", command=self.add_transaction)
        submit_btn.grid(row=5, column=0, columnspan=2, pady=10)
        
    def create_transaction_list(self):
        # Transaction list frame
        list_frame = ttk.LabelFrame(self.left_frame, text="Recent Transactions")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create treeview
        self.tree = ttk.Treeview(list_frame, columns=('Date', 'Category', 'Amount', 'Type', 'Description'))
        self.tree.heading('Date', text='Date')
        self.tree.heading('Category', text='Category')
        self.tree.heading('Amount', text='Amount')
        self.tree.heading('Type', text='Type')
        self.tree.heading('Description', text='Description')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack elements
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.update_transaction_list()
        
    def create_summary(self):
        # Summary frame
        summary_frame = ttk.LabelFrame(self.right_frame, text="Summary")
        summary_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add summary labels
        self.total_income_label = ttk.Label(summary_frame, text="Total Income: $0")
        self.total_income_label.pack(pady=5)
        
        self.total_expense_label = ttk.Label(summary_frame, text="Total Expenses: $0")
        self.total_expense_label.pack(pady=5)
        
        self.balance_label = ttk.Label(summary_frame, text="Balance: $0")
        self.balance_label.pack(pady=5)
        
        # Create and pack the chart
        self.create_chart()
        
    def create_chart(self):
        # Create matplotlib figure
        self.figure, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.right_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.update_chart()
        
    def add_transaction(self):
        try:
            date = self.date_entry.get()
            category = self.category_combobox.get()
            amount = float(self.amount_entry.get())
            description = self.description_entry.get()
            type = self.type_combobox.get()
            
            add_transaction(date, category, amount, description, type)
            
            # Clear form
            self.amount_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)
            
            # Update display
            self.update_transaction_list()
            self.update_summary()
            self.update_chart()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")
            
    def update_transaction_list(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Add transactions to tree
        for transaction in get_transactions():
            self.tree.insert('', 'end', values=transaction[1:])
            
        self.update_summary()
        
    def update_summary(self):
        transactions = get_transactions()
        
        total_income = sum(t[3] for t in transactions if t[5] == 'income')
        total_expenses = sum(t[3] for t in transactions if t[5] == 'expense')
        balance = total_income - total_expenses
        
        self.total_income_label.config(text=f"Total Income: ${total_income:.2f}")
        self.total_expense_label.config(text=f"Total Expenses: ${total_expenses:.2f}")
        self.balance_label.config(text=f"Balance: ${balance:.2f}")
        
    def update_chart(self):
        transactions = get_transactions()
        
        # Clear previous chart
        self.ax.clear()
        
        # Prepare data for chart
        categories = {}
        for transaction in transactions:
            if transaction[5] == 'expense':  # Only show expenses in the chart
                category = transaction[2]
                amount = transaction[3]
                categories[category] = categories.get(category, 0) + amount
                
        if categories:
            # Create pie chart
            labels = list(categories.keys())
            sizes = list(categories.values())
            self.ax.pie(sizes, labels=labels, autopct='%1.1f%%')
            self.ax.set_title('Expense Distribution')
            
        self.canvas.draw() 