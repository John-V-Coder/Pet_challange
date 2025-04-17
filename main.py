from pet import Pet

def show_menu():
    print("\nWhat would you like to do?")
    print("1. Feed your pet")
    print("2. Let your pet sleep")
    print("3. Play with your pet")
    print("4. Check pet status")
    print("5. Teach a trick")
    print("6. Show learned tricks")
    print("0. Save and Exit")

def main():
    name = input("🐶 What's your pet's name? ")
    pet = Pet.load_from_file(name)

    action_count = 0  # Track number of actions since last save

    while True:
        show_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            pet.eat()
        elif choice == "2":
            pet.sleep()
        elif choice == "3":
            pet.play()
        elif choice == "4":
            pet.get_status()
        elif choice == "5":
            trick = input("What trick would you like to teach? ")
            pet.train(trick)
        elif choice == "6":
            pet.show_tricks()
        elif choice == "0":
            pet.save_to_file()
            print(f"Goodbye from {pet.name}! 🐾")
            break
        else:
            print("Invalid choice. Try again!")
            continue

        # Count real actions only (not status or show_tricks)
        if choice in ["1", "2", "3", "5"]:
            action_count += 1

        # Autosave every 3 actions
        if action_count >= 3:
            pet.save_to_file()
            print("🛟 Autosaved!")
            action_count = 0

if __name__ == "__main__":
    main()
