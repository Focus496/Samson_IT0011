class Item:
    def __init__(self, id, name, description, price):
        self.id = id
        self.name = name
        self.description = description
        self.price = price

def add_item(item_list, new_item):
    """Adds a new item to the list after validation."""
    if not isinstance(new_item.id, int) or any(item.id == new_item.id for item in item_list):
        return "ID must be a unique integer."
    if not isinstance(new_item.name, str) or not new_item.name:
        return "Name must be a non-empty string."
    if not isinstance(new_item.description, str):
        return "Description must be a string."
    if not isinstance(new_item.price, (int, float)) or new_item.price <= 0:
        return "Price must be a positive number."

    item_list.append(new_item)
    return "Item added successfully!"

def display_items(item_list):
    """Displays all items in the list."""
    print("\n--- Item List ---")
    if not item_list:
        print("No items available.")
    else:
        for item in item_list:
            print(f"ID: {item.id}, Name: {item.name}, Description: {item.description}, Price: ${item.price:.2f}")
    print("------------------")

def menu():
    """Displays a menu for user interaction."""
    item_list = []

    while True:
        print("\nMenu:")
        print("1. Add an Item")
        print("2. View Items")
        print("3. Exit")

        choice = input("Please Enter your choice: ").strip()

        if choice == "1":
            try:
                id = int(input("Enter item ID: ").strip())
                name = input("Enter item name: ").strip()
                description = input("Enter item description: ").strip()
                price = float(input("Enter item price: ").strip())

                new_item = Item(id, name, description, price)
                print(add_item(item_list, new_item))

            except ValueError:
                print("Invalid input")

        elif choice == "2":
            display_items(item_list)

        elif choice == "3":
            print("Exiting program")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    menu()
