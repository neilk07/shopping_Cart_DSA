import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Class to represent a product
class Product:
    def __init__(self, name, price, category, subcategory):
        self.name = name
        self.price = price
        self.category = category
        self.subcategory = subcategory

# Class for a node in the binary search tree
class BSTNode:
    def __init__(self, product):
        self.product = product
        self.left = None
        self.right = None

# Class for the product catalog using a binary search tree
class ProductCatalog:
    def __init__(self):
        self.root = None

    def insert(self, product):
        self.root = self._insert(self.root, product)

    def _insert(self, node, product):
        if node is None:
            return BSTNode(product)

        if product.name < node.product.name:
            node.left = self._insert(node.left, product)
        elif product.name > node.product.name:
            node.right = self._insert(node.right, product)

        return node

    def search(self, product_name):
        return self._search(self.root, product_name)

    def _search(self, node, product_name):
        if node is None or node.product.name == product_name:
            return node.product if node else None

        if product_name < node.product.name:
            return self._search(node.left, product_name)
        else:
            return self._search(node.right, product_name)

# Class for a shopping cart
class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, product, quantity):
        self.items.append({"product": product, "quantity": quantity})

    def remove_item(self, product_name):
        for item in self.items:
            if item["product"].name == product_name:
                self.items.remove(item)
                break

    def get_total_price(self):
        return sum(item["product"].price * item["quantity"] for item in self.items)

# Class for the GUI of the shopping cart
class ShoppingCartGUI:
    def __init__(self, master, catalog):
        self.master = master
        self.master.title("Dynamic Shopping Cart")
        self.catalog = catalog
        self.cart = ShoppingCart()
        
        self.selected_index = tk.IntVar(value=-1)

        # Create the product selection widgets
        self.product_var = tk.StringVar()
        self.product_var.set("")
        self.product_menu = ttk.Combobox(self.master, textvariable=self.product_var)
        self.product_menu["values"] = list(set(product.subcategory for product in self.catalog_in_order_traversal()))
        self.product_menu.set(self.product_menu["values"][0] if self.product_menu["values"] else "")
        self.product_menu.pack()

        self.quantity_label = ttk.Label(self.master, text="Quantity:")
        self.quantity_label.pack()

        self.quantity_spinbox = tk.Spinbox(self.master, from_=1, to=10)
        self.quantity_spinbox.pack()

        self.add_button = ttk.Button(self.master, text="Add to Cart", command=self.add_to_cart)
        self.add_button.pack()
        
        self.remove_button = ttk.Button(self.master, text="Remove from Cart", command=self.remove_from_cart)
        self.remove_button.pack()

        # Create the cart display widgets
        self.cart_label = ttk.Label(self.master, text="Cart:")
        self.cart_label.pack()

        self.cart_listbox = tk.Listbox(self.master)
        self.cart_listbox.pack()
        self.cart_listbox.bind("<<ListboxSelect>>", self.on_cart_select)

        self.total_label = ttk.Label(self.master, text="Total: Rs. 0.00")
        self.total_label.pack()
        
        self.product_indices = {}

    def add_to_cart(self):
        subcategory = self.product_var.get()
        product = next((p for p in self.catalog_in_order_traversal() if p.subcategory == subcategory), None)
        quantity = int(self.quantity_spinbox.get())

        if product:
            self.cart.add_item(product, quantity)
            self.cart_listbox.insert(tk.END, f"{product.name} x {quantity}")
            self.total_label.config(text=f"Total: Rs. {self.cart.get_total_price():.2f}")
            
            self.update_product_indices()
            
    def on_cart_select(self, event):
        selected_index = self.selected_index.get()

        if selected_index >= 0:
            self.selected_index = selected_index
            self.cart_listbox.delete(self.selected_index)
            self.cart.remove_item(self.selected_index)
            self.total_label.config(text=f"Total: Rs. {self.cart.get_total_price():.2f}")

    def update_product_indices(self):
        # Update the mapping between each product name and its index in the Listbox.
        self.product_indices = {}
        for idx in range(self.cart_listbox.size()):
            product_name = self.cart_listbox.get(idx).split(' x ')[0]
            self.product_indices[product_name] = idx
            
    def remove_from_cart(self):
        selected_index = self.cart_listbox.curselection()

        if selected_index:
            index = int(selected_index[0])
            product_name = self.cart_listbox.get(index).split(' x ')[0]
            self.cart.remove_item(product_name)
            self.cart_listbox.delete(selected_index)
            self.total_label.config(text=f"Total: Rs. {self.cart.get_total_price():.2f}")
        else:
            messagebox.showinfo(title="Error", message="Please select an item to remove from the cart.")

    def catalog_in_order_traversal(self):
        return self._in_order_traversal(self.catalog.root)

    def _in_order_traversal(self, node):
        if node is not None:
            yield from self._in_order_traversal(node.left)
            yield node.product
            yield from self._in_order_traversal(node.right)

def main():
    # Sample product data for the catalog
    product_data = [
        ("Men", "Clothing", "Shirt", "Product A", 3000),
        ("Men", "Clothing", "Pants", "Product B", 4000),
        ("Women", "Clothing", "Dress", "Product C", 7000),
        ("Women", "Footwear", "Shoes", "Product D", 4000),
        ("Women", "Accessories", "Handbag", "Product E", 5000)
    ]

    # Initialize the product catalog using a binary search tree
    catalog = ProductCatalog()
    for category, subcategory1, subcategory2, name, price in product_data:
        product = Product(name, price, category, f"{subcategory1} > {subcategory2}")
        catalog.insert(product)

    root = tk.Tk()
    app = ShoppingCartGUI(root, catalog)
    root.mainloop()

if __name__ == "__main__":
    main()
