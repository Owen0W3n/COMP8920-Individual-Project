import json
import os
from products import KeyboardKit, Keycap, Switch, Product


class Inventory:
    def __init__(self):
        self.__products = []


    def get_all_products(self) -> list:
        return self.__products[:]

    def get_by_category(self, category: str) -> list:
        return [p for p in self.__products if p.category().lower() == category.lower()]


    def add_product(self, product: Product) -> None:
        existing = self.find_product(product.name, product.category())
        if existing:
            existing.increase_quantity(product.quantity)
        else:
            self.__products.append(product)


    def find_product(self, name: str, category: str = None):
        for product in self.__products:
            same_name = product.name.lower() == name.lower()
            if category is None:
                same_category = True
            else:
                same_category = product.category().lower() == category.lower()
            if same_name and same_category:
                return product
        return None

    def display_all_products(self) -> None:
        if not self.__products:
            print("No products available.")
            return

        print("\n=== ALL PRODUCTS ===")
        for index, product in enumerate(sorted(self.__products), start=1):
            print(f"{index}. {product}")

    def display_category(self, category: str) -> None:
        products = self.get_by_category(category)
        if not products:
            print(f"No products found in category: {category}")
            return

        print(f"\n=== {category.upper()} ===")
        for index, product in enumerate(products, start=1):
            print(f"{index}. {product}")

    def create_product_viewchoice(self):
        print("\nChoose category to add:")
        print("1. Keyboard Kit")
        print("2. Keycaps")
        print("3. Switches")


        choice = input("Enter choice: ").strip()



        name = input("Product name: ").strip()
        price = self._read_float("Price: ")
        quantity = self._read_int("Quantity: ")


        if choice == "1":
            layout = input("Layout (60%, 65%, 75%, TKL, 100%): ").strip()
            product = KeyboardKit(name, price, quantity, layout)

        elif choice == "2":
            profile = input("Profile: ").strip()
            product = Keycap(name, price, quantity, profile)

        elif choice == "3":
            switch_type = input("Switch type (Linear / Tactile / Clicky): ").strip()
            product = Switch(name, price, quantity, switch_type)

        else:
            print("Invalid category choice.")
            return False

        self.add_product(product)
        print(f"Product '{name}' added/updated successfully.")
        return True

    def save_to_json(self, filename: str) -> None:
        data = [product.to_dict() for product in self.__products]
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def load_from_json(self, filename: str) -> bool:
        if not os.path.exists(filename):
            return False

        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.__products.clear()

        for product_data in data:
            product = Product.from_dict(product_data)
            self.__products.append(product)

        return True

    @staticmethod
    def _read_int(prompt: str) -> int:
        while True:
            try:
                value = int(input(prompt))
                if value < 0:
                    print("Please enter a non-negative integer.")
                    continue
                return value
            except ValueError:
                print("Invalid integer. Try again.")

    @staticmethod
    def _read_float(prompt: str) -> float:
        while True:
            try:
                value = float(input(prompt))
                if value < 0:
                    print("Please enter a non-negative price.")
                    continue
                return value
            except ValueError:
                print("Invalid number. Try again.")
