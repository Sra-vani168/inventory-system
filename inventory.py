import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Database setup
def init_db():
    conn = sqlite3.connect("inventory.db")  # Ensure this line is indented
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# Function to add a product
# Function to add a product
def add_product():
    name = name_entry.get()
    quantity = quantity_entry.get()
    price = price_entry.get()
    
    if name and quantity.isdigit() and price.replace(".", "", 1).isdigit():
        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO inventory (product_name, quantity, price) VALUES (?, ?, ?)", 
                       (name, int(quantity), float(price)))
        conn.commit()
        conn.close()
        display_products()
        clear_entries()
    else:
        messagebox.showerror("Input Error", "Please enter valid data!")


# Function to display products
# Function to display products
def display_products():
    for row in tree.get_children():  # Ensure this line is indented
        tree.delete(row)
    
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventory")
    rows = cursor.fetchall()
    conn.close()
    
    for row in rows:
        tree.insert("", "end", values=row)

# Function to clear entry fields
# Function to clear entry fields
def clear_entries():
    name_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)

# Function to delete selected product
def delete_product():
    selected_item = tree.selection()
    if selected_item:
        item = tree.item(selected_item)
        product_id = item['values'][0]
        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM inventory WHERE id = ?", (product_id,))
        conn.commit()
        conn.close()
        display_products()
    else:
        messagebox.showerror("Selection Error", "Please select a product to delete!")
# Function to update selected product
# Function to update selected product
def update_product():
    selected_item = tree.selection()
    if selected_item:
        item = tree.item(selected_item)
        product_id = item['values'][0]
        new_name = name_entry.get()
        new_quantity = quantity_entry.get()
        new_price = price_entry.get()
        
        if new_name and new_quantity.isdigit() and new_price.replace(".", "", 1).isdigit():
            conn = sqlite3.connect("inventory.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE inventory SET product_name = ?, quantity = ?, price = ? WHERE id = ?", 
                           (new_name, int(new_quantity), float(new_price), product_id))
            conn.commit()
            conn.close()
            display_products()
            clear_entries()
        else:
            messagebox.showerror("Input Error", "Please enter valid data!")
    else:
        messagebox.showerror("Selection Error", "Please select a product to update!")

# GUI Setup
root = tk.Tk()
root.title("Inventory Management System")
root.geometry("600x450")

init_db()

# Input fields
tk.Label(root, text="Product Name").pack()
name_entry = tk.Entry(root)
name_entry.pack()

tk.Label(root, text="Quantity").pack()
quantity_entry = tk.Entry(root)
quantity_entry.pack()

tk.Label(root, text="Price").pack()
price_entry = tk.Entry(root)
price_entry.pack()

tk.Button(root, text="Add Product", command=add_product).pack()
tk.Button(root, text="Update Product", command=update_product).pack()
tk.Button(root, text="Delete Product", command=delete_product).pack()

# Table to display inventory
tree = ttk.Treeview(root, columns=("ID", "Name", "Quantity", "Price"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Quantity", text="Quantity")
tree.heading("Price", text="Price")
tree.pack()

display_products()

root.mainloop()
