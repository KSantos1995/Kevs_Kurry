from utils import save_data, close_program
import time

class Options_Menu:
    # Constructor for menu.
    def __init__(self):
        self.options = [
            {   
                "id" : 1,
                "title" : "View Menu"
            },
            {
                "id" : 2,
                "title" : "Add Item to Menu"
            },
            {
                "id" : 3,
                "title" : "Remove Item from Menu"
            },
            {
                "id" : 4,
                "title" : "Save data to JSON"
            },
            {
                "id" : 5,
                "title" : "Exit Program"
            }
        ]
