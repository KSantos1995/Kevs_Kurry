from utils import save_data, close_program
import time

class Options_Menu:
    # Constructor for menu.
    def __init__(self):
        self.options = [
            {   
                "id" : 1,
                "title" : "View Menu",
                "execute" : self.view_menu
            },
            {
                "id" : 2,
                "title" : "Add Item to Menu",
                "execute" : self.add_menu_item
            },
            {
                "id" : 3,
                "title" : "Save data to JSON",
                "execute" : save_data
            },
            {
                "id" : 4,
                "title" : "Exit Program",
                "execute" : close_program
            }
        ]

    def welcome_user(self, restaurant_name):
            print("\n")
            print("##################################################")
            print(f"######### Welcome to {restaurant_name} #################")
            print("##################################################\n")

    def display_options(self):
        print("##################################################")
        print(f"############### Menu Options ####################")
        print("##################################################\n") 
        print("What would you like to do today? \n")       
        for option in self.options:
            print(f"Option {option['id']}: {option['title']}")

    def view_menu(self, menu_categories):
        print("##################################################")
        print(f"############# Menu Breakdown ##################")
        print("##################################################\n")
        for i in range(len(menu_categories)): 
            category_name = menu_categories[i]['category']
            category_items = menu_categories[i]['items']
            print(f"- - - Special Selection of {category_name}'s for the day \n")
            for item in category_items:
                time.sleep(0.2)
                print(f"Item {item['id']}: {item['name']} ... Price: ${item['price']}")
            print("\n")

    def handle_options(self, restaurant_data, options, file_path):
        menu_categories = restaurant_data['menu']
        user_choice = input("\nPlease enter either the Option ID or the Option Title: ")
        self.execute_user_option(restaurant_data, menu_categories, options, user_choice, file_path)

    def execute_user_option(self, restaurant_data, menu_categories, options, user_choice, file_path):
        user_choice = user_choice.strip()
        for option in options:
            if option['id'] == int(user_choice.strip()) or option['title'].lower() == user_choice.lower():
                if option['id'] == 3:
                    option['execute'](file_path, restaurant_data)
                else:
                    option['execute'](menu_categories)
                return    
        print("Option was not found. Please try again. \n")
        self.handle_options(restaurant_data, options, file_path)

    def add_menu_item(self, menu_categories):
        print("##################################################")
        print(f"############# Adding Menu Item  ##################")
        print("##################################################\n")

        for i in range(len(menu_categories)):
            print(f"Option {i+1}: {menu_categories[i]['category']}\n")

        user_choice = input("Enter either the Option ID or the Menu Category Name: ").strip().lower()

        for i in range(len(menu_categories)):
            current_category = menu_categories[i]
            category_name = current_category['category']
            category_id = current_category['id']
            category_items = current_category['items']

            if user_choice.lower() == category_name.lower() or user_choice == str(category_id):
                print(f"What would you like to add to your {category_name} Menu?")
                new_item_name = input(f"Enter item name here: ")
                new_item_price = float(input("Enter item price: $").strip())
                category_items.append({
                    "id" : category_items[-1]['id'] + 1,
                    "name" : new_item_name,
                    "price" : new_item_price
                })
                self.update_ids(menu_categories)

    def update_ids(self, menu_categories):
        item_index = 1
        for i in range(len(menu_categories)): 
            category_name = menu_categories[i]['category']
            category_items = menu_categories[i]['items']
            for item in category_items:
                item['id'] = item_index 
                item_index += 1

    def check_continue_status(self, run_program):
        response = input("Would you like to continue using our program's features? (Yes/No)")
        if response.strip().lower() == "yes":
            return True
        elif response.strip().lower() == "no":
            return False
        else:
            second_response = input("Please try again with either Yes or No as your entry. If your submission is invalid, program will end")
            if second_response.strip().lower() == "yes":
                return True
            else:
                run_program = False
        return run_program
    
    def run(self, restaurant_data, file_path):
        self.display_options()
        self.handle_options(restaurant_data, self.options, file_path)