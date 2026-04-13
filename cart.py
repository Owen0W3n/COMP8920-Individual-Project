from products import Product


class CartItem:
    def __init__(self, product: Product, quantity: int = 1):
        self.product = product
        self.quantity = quantity

    @property
    def subtotal(self) -> float:
        return self.product.price * self.quantity

    def __str__(self) -> str:
        return (
            f"{self.product.category():15} | {self.product.name:25} | "
            f"Qty: {self.quantity:<3} | Subtotal: ${self.subtotal:.2f}"
        )


class ShoppingCart:
    REQUIRED_CATEGORIES = {"Keyboard Kit", "Keycaps", "Switches"}

    def __init__(self):
        self.__items = []

    def add_item(self, product: Product, quantity: int = 1) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0.")

        for item in self.__items:
            if item.product == product:
                item.quantity += quantity
                return

        self.__items.append(CartItem(product, quantity))

    def remove_item(self, product_name: str) -> bool:
        for item in self.__items:
            if item.product.name.lower() == product_name.lower():
                self.__items.remove(item)
                return True
        return False

    def get_items(self) -> list:
        return self.__items[:]

    def is_empty(self) -> bool:
        return len(self.__items) == 0

    def categories_in_cart(self) -> set:
        return {item.product.category() for item in self.__items}

    def can_checkout(self) -> bool:
        return self.REQUIRED_CATEGORIES.issubset(self.categories_in_cart())

    def total(self) -> float:
        return sum(item.subtotal for item in self.__items)

    def clear(self) -> None:
        self.__items.clear()

    def display_cart(self) -> None:
        if self.is_empty():
            print("Shopping cart is empty.")
            return

        print("\n=== SHOPPING CART ===")
        for i, item in enumerate(self.__items, start=1):
            print(f"{i}. {item}")
        print(f"Total: ${self.total():.2f}")

        missing = self.REQUIRED_CATEGORIES - self.categories_in_cart()
        if missing:
            print("Cannot checkout yet. Missing categories:")
            for category in missing:
                print(f"- {category}")

    def __len__(self) -> int:
        return len(self.__items)

    def __iter__(self):
        return iter(self.__items)
