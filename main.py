from fastmcp import FastMCP
import os
import sqlite3
import json

DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")

CATEGORIES_PATH = os.path.join(os.path.dirname(__file__), "category.json")

mcp= FastMCP(name="Expense Tracker")

@mcp.tool
def init_db():
    """Initialize the database and create the expenses table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            notes TEXT
        )
        """
    )
    conn.commit()
    conn.close()
    return {"message": "Database initialized successfully."}

@mcp.tool
def add_expense(date: str, amount: float, category: str, description: str, notes:str = None):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO expenses (date, amount, category, description, notes) VALUES (?, ?, ?, ?, ?)",
            (date, amount, category, description, notes),
        )
        conn.commit()

    return {"message": "Expense added successfully."}

@mcp.tool
def list_expenses(start_date: str | None = None, end_date: str | None = None):
    """List expenses, optionally filtered by an inclusive YYYY-MM-DD date range."""
    query = "SELECT * FROM expenses"
    params = []
    conditions = []

    if start_date:
        conditions.append("date >= ?")
        params.append(start_date)

    if end_date:
        conditions.append("date <= ?")
        params.append(end_date)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY date ASC, id ASC"

    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, params)
        expenses = [dict(row) for row in cursor.fetchall()]

    return {"expenses": expenses}

@mcp.tool
def summarize(start_date: str | None = None, end_date: str | None = None):
    """Summarize expenses by category, optionally filtered by an inclusive YYYY-MM-DD date range."""
    query = "SELECT category, SUM(amount) as total_amount FROM expenses"
    params = []
    conditions = []

    if start_date:
        conditions.append("date >= ?")
        params.append(start_date)

    if end_date:
        conditions.append("date <= ?")
        params.append(end_date)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " GROUP BY category ORDER BY total_amount DESC"

    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, params)
        summary = [dict(row) for row in cursor.fetchall()]

    return {"summary": summary}

@mcp.resource("expense-categories://categories", mime_type="application/json")
def categories():
    """Read the expense categories from category.json."""
    with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    mcp.run(
        transport="http",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000")),
    )
