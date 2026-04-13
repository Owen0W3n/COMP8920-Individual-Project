from store import KeyboardStore

# Menu for the application
1
def menu():
    print("\n========== KEYBOARD STORE ==========")
    print("1. View all products")
    print("2. View products by category")
    print("3. Build a keyboard")
    print("4. Add new product to inventory")
    print("5. Add item to shopping cart")
    print("6. View shopping cart")
    print("7. Checkout")
    print("0. Exit")
    print("====================================")

#Controller lead to different function user want to use
def main():
    store = KeyboardStore()

    while True:
        menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            store.view_products()
        elif choice == "2":
            store.view_products_by_category()
        elif choice == "3":
            store.build_keyboard()
        elif choice == "4":
            store.add_product_to_inventory()
        elif choice == "5":
            store.add_to_cart()
        elif choice == "6":
            store.display_cart()
        elif choice == "7":
            store.checkout()
        elif choice == "0":
            print("Thank you for using Keyboard Store.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
