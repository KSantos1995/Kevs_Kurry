import json
import time
from options_menu import Options_Menu
from utils import load_data


def main():
    # Path from root directory to JSON file
    file_path = "../data/restaurant_data.json"
    # Default True to run program. Set to false when program is over.
    run_program = True
    # Create instance of Options_Menu
    options_menu = Options_Menu()
    # Load data and grabs Restaurant Name
    restaurant_data = load_data(file_path)
    restaurant_name = restaurant_data['name']
    # Welcome user with Restaurant Name
    options_menu.welcome_user(restaurant_name)
    # Run_program default to True
    while run_program:
        # Calls for menu option to execute
        options_menu.run(restaurant_data, file_path)
        # After each option, we check if user wants to use another option
        run_program = options_menu.check_continue_status(run_program)
    print("--- End Of Program ---")

if __name__ == "__main__":
    main()