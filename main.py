import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime
from dashboard import Dashboard
from database import initialize_database

class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Dashboard")
        self.root.geometry("800x600")
        
        # Initialize database
        initialize_database()
        
        # Create main container
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Initialize dashboard
        self.dashboard = Dashboard(self.main_container)

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop() 