from inventory import Inventory
from cart import ShoppingCart
from products import KeyboardKit, Keycap, Switch


class KeyboardStore:
    INVENTORY_FILE = "inventory.json"

    def __init__(self):
        self.inventory = Inventory()
        self.cart = ShoppingCart()

        loaded = self.inventory.load_from_json(self.INVENTORY_FILE)
        if not loaded:
            self._load_default_product()
            self.inventory.save_to_json(self.INVENTORY_FILE)

    def _load_default_product(self):
        self.inventory.add_product(KeyboardKit("Mode Envoy (Mirage/ Copper)", 195.00, 10, "65%"))
        self.inventory.add_product(KeyboardKit("TOFU 60 3.0 (Anodized Black)", 161.00, 8, "60%"))
        self.inventory.add_product(KeyboardKit("HOLY 80 (E-White)", 172.00, 6, "80%"))

        self.inventory.add_product(Keycap("PBT Black on White", 49.90, 15, "Cherry"))
        self.inventory.add_product(Keycap("GMK Blue Samurai Clone", 59.90, 12, "OEM"))
        self.inventory.add_product(Keycap("XDA Matcha Set", 39.90, 9, "XDA"))

        self.inventory.add_product(Switch("Gateron Milky Yellow", 24.90, 30, "Linear"))
        self.inventory.add_product(Switch("Boba U4T", 39.90, 20, "Tactile"))
        self.inventory.add_product(Switch("Y-3", 34.90, 18, "Linear"))

    def view_products(self):
        self.inventory.display_all_products()

    def view_products_by_category(self):
        print("\nView by category:")
        print("1. Keyboard Kit")
        print("2. Keycaps")
        print("3. Switches")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            self.inventory.display_category("Keyboard Kit")
        elif choice == "2":
            self.inventory.display_category("Keycaps")
        elif choice == "3":
            self.inventory.display_category("Switches")
        else:
            print("Invalid choice.")

    def build_keyboard(self):
        print("\n=== BUILD YOUR KEYBOARD ===")
        selected_items = []

        for category in ["Keyboard Kit", "Keycaps", "Switches"]:
            self.inventory.display_category(category)
            name = input(f"Enter the {category} name you want (enter E if you want to exit): ").strip()

            if name.lower() == "e":
                return

            product = self.inventory.find_product(name, category)

            if not product:
                print(f"{category} '{name}' not found.")
                return

            if product.quantity < 1:
                print(f"{product.name} is out of stock.")
                return

            selected_items.append(product)

        print("\nKeyboard build selected successfully:")
        total = 0.0
        for item in selected_items:
            print(f"- {item.name} ({item.category()}) - ${item.price:.2f}")
            total += item.price
        print(f"Build total: ${total:.2f}")

        add_to_cart = input("Add this full build to cart? (y/n): ").strip().lower()
        if add_to_cart == "y":
            for item in selected_items:
                self.cart.add_item(item, 1)
            print("Complete keyboard build added to cart.")

    def add_product_to_inventory(self):
        added = self.inventory.create_product_viewchoice()
        if added:
            self.inventory.save_to_json(self.INVENTORY_FILE)

    def add_to_cart(self):
        print("\nAdd product to cart:")
        print("1. Keyboard Kit")
        print("2. Keycaps")
        print("3. Switches")
        choice = input("Enter choice: ").strip()

        mapping = {
            "1": "Keyboard Kit",
            "2": "Keycaps",
            "3": "Switches"
        }

        category = mapping.get(choice)
        if not category:
            print("Invalid category choice.")
            return

        self.inventory.display_category(category)
        name = input("Enter product name: ").strip()
        quantity = self._read_int("Enter quantity: ")

        product = self.inventory.find_product(name, category)
        if not product:
            print("Product not found.")
            return

        if product.quantity < quantity:
            print("Not enough stock available.")
            return

        self.cart.add_item(product, quantity)
        print(f"{quantity} x {product.name} added to cart.")

    def checkout(self):
        print("\n=== CHECKOUT ===")
        self.cart.display_cart()

        if self.cart.is_empty():
            return

        if not self.cart.can_checkout():
            print("Checkout denied. You must have at least one item from all 3 categories.")
            return

        confirm = input("Confirm checkout? (y/n): ").strip().lower()
        if confirm != "y":
            print("Checkout cancelled.")
            return

        try:
            for item in self.cart:
                item.product.decrease_quantity(item.quantity)
        except ValueError as error:
            print(f"Checkout failed: {error}")
            return

        self.inventory.save_to_json(self.INVENTORY_FILE)
        print(f"Payment successful. Total paid: ${self.cart.total():.2f}")
        self.cart.clear()

    def display_cart(self):
        self.cart.display_cart()

    @staticmethod
    def _read_int(prompt: str) -> int:
        while True:
            try:
                value = int(input(prompt))
                if value <= 0:
                    print("Please enter an integer greater than 0.")
                    continue
                return value
            except ValueError:
                print("Invalid integer. Try again.")
