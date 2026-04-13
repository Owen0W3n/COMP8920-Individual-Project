from abc import ABC, abstractmethod


class Product(ABC):
    #Abstract object calss that define common attributes and behavior for all products
    def __init__(self, name: str, price: float, quantity: int):
        self._name = name
        self._price = price
        self._quantity = quantity

    @property
    def name(self) -> str:
        return self._name

    @property
    def price(self) -> float:
        return self._price

    @property
    def quantity(self) -> int:
        return self._quantity

    def increase_quantity(self, amount: int):
        # Prevent invalid negative input
        if amount < 0:
            raise ValueError("Amount to increase cannot be negative.")
        # Add stock
        self._quantity += amount

    def decrease_quantity(self, amount: int):
        if amount < 0:
            raise ValueError("Amount to decrease cannot be negative.")
        if amount > self._quantity:
            raise ValueError(f"Not enough stock for {self._name}.")
        self._quantity -= amount

    @abstractmethod
    #each subclass need to implement this
    def category(self) -> str:
        pass

    def to_dict(self) -> dict:
        #transfter object into dictionary for JSON to store
        return {
            "category": self.category(),
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
        }

    @staticmethod
    def from_dict(data: dict):
        category = data["category"]

        if category == "Keyboard Kit":
            return KeyboardKit(
                data["name"],
                data["price"],
                data["quantity"],
                data["layout"]
            )
        elif category == "Keycaps":
            return Keycap(
                data["name"],
                data["price"],
                data["quantity"],
                data["profile"]
            )
        elif category == "Switches":
            return Switch(
                data["name"],
                data["price"],
                data["quantity"],
                data["switch_type"]
            )
        else:
            raise ValueError(f"Unknown category: {category}")

    def __str__(self) -> str:
        # define how object should be printed
        return f"{self.category():15} | {self._name:25} | ${self._price:8.2f} | Stock: {self._quantity}"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(name={self._name!r}, price={self._price}, quantity={self._quantity})"
        )

    def __eq__(self, other) -> bool:
        if not isinstance(other, Product):
            return False
        return self.name.lower() == other.name.lower() and self.category() == other.category()

    def __lt__(self, other) -> bool:
        if not isinstance(other, Product):
            return NotImplemented
        return self.price < other.price


class KeyboardKit(Product):
    #inherit the common attribute and function from product
    def __init__(self, name: str, price: float, quantity: int, layout: str):
        super().__init__(name, price, quantity)
        self._layout = layout

    @property
    def layout(self) -> str:
        return self._layout

    def category(self) -> str:
        return "Keyboard Kit"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["layout"] = self.layout
        return data

    def __str__(self) -> str:
        return (
            f"{self.category():20} | {self.name:30} | Layout: {self.layout:11} "
            f"| ${self.price:13.2f} | Stock: {self.quantity}"
        )

#adding distinct attribute for different category
class Keycap(Product):
    def __init__(self, name: str, price: float, quantity: int, profile: str):
        super().__init__(name, price, quantity)
        self._profile = profile

    @property
    def profile(self) -> str:
        return self._profile

    def category(self) -> str:
        return "Keycaps"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["profile"] = self.profile
        return data

    def __str__(self) -> str:
        return (
            f"{self.category():20} | {self.name:30} | Profile: {self.profile:11} "
            f"| ${self.price:13.2f} | Stock: {self.quantity}"
        )


class Switch(Product):
    def __init__(self, name: str, price: float, quantity: int, switch_type: str):
        super().__init__(name, price, quantity)
        self._switch_type = switch_type

    @property
    def switch_type(self) -> str:
        return self._switch_type

    def category(self) -> str:
        return "Switches"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["switch_type"] = self.switch_type
        return data

    def __str__(self) -> str:
        return (
            f"{self.category():20} | {self.name:30} | Type: {self.switch_type:14} "
            f"| ${self.price:13.2f} | Stock: {self.quantity}"
        )
