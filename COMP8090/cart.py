from products import Product


class CartItem:
    def __init__(self, product: Product, quantity: int = 1):
         # store the actual product object
        self.product = product
        self.quantity = quantity

    @property
    def subtotal(self) -> float:
        # calculate the total price for this cart item
        return self.product.price * self.quantity

    def __str__(self) -> str:
        #how a CartItem should be displayed when printed
        return (
            f"{self.product.category():15} | {self.product.name:25} | "
            f"Qty: {self.quantity:<3} | Subtotal: ${self.subtotal:.2f}"
        )


class ShoppingCart:
     # these are the categories required before checkout is allowed if building keyboard option is chose
    REQUIRED_CATEGORIES = {"Keyboard Kit", "Keycaps", "Switches"}

    def __init__(self):
        self.__items = []

    def add_item(self, product: Product, quantity: int = 1) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0.")

        # check whether the product is already in the cart
        for item in self.__items:
            if item.product == product:
                item.quantity += quantity
                return

        self.__items.append(CartItem(product, quantity))

    def remove_item(self, product_name: str) -> bool:
        for item in self.__items:
            if item.product.name.lower() == product_name.lower():
                #remove matching item
                self.__items.remove(item)
                return True
        return False

    def get_items(self) -> list:
        return self.__items[:]

    def is_empty(self) -> bool:
        return len(self.__items) == 0

    def categories_in_cart(self) -> set:
        return {item.product.category() for item in self.__items}
        #return all product categories currently in the cart

    def can_checkout(self) -> bool:
        return self.REQUIRED_CATEGORIES.issubset(self.categories_in_cart())
        #only allowing checkout when all category is fufiled in the shopping cart

    def total(self) -> float:
        return sum(item.subtotal for item in self.__items)

    def clear(self) -> None:
        self.__items.clear()

    def display_cart(self) -> None:
        #checking whether the cart is empty or not 
        if self.is_empty():
            print("Shopping cart is empty.")
            return

        print("\n=== SHOPPING CART ===")
        #display the items in cart
        for i, item in enumerate(self.__items, start=1):
            print(f"{i}. {item}")
        print(f"Total: ${self.total():.2f}")

        #check and print if some categories are missing
        missing = self.REQUIRED_CATEGORIES - self.categories_in_cart()
        if missing:
            print("Cannot checkout yet. Missing categories:")
            for category in missing:
                print(f"- {category}")

    def __len__(self) -> int:
        #allow to return number of cart rows
        return len(self.__items)

    def __iter__(self):
        #allow iteration
        return iter(self.__items)
