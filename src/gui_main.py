import customtkinter as ctk
from options_menu import Options_Menu
from utils import update_ids, load_data, save_data, close_program

class Restaurant_GUI:

    # Constructor for App contentbar and sidebar components
    def __init__(self, root, file_path):
        self.root = root
        self.file_path = file_path
        self.options_menu = Options_Menu()
        self.restaurant_data = load_data(file_path)

        self.root.title("")
        self.root.geometry("570x600")

        # Sidebar for buttons
        self.sidebar = ctk.CTkFrame(root, width=150, border_width=3, border_color="white", fg_color="light blue")
        self.sidebar.pack(side="left", fill="y")

        # Main content area
        self.content_frame = ctk.CTkFrame(root, fg_color="light blue")
        self.content_frame.pack(side="right", expand=True, fill="both")

        # Welcome Label in content area
        self.welcome_label = ctk.CTkLabel(
            self.content_frame, 
            text=f"Welcome to {self.restaurant_data['name']}!",
            font=("Arial", 20)
        )
        self.welcome_label.pack(pady=20)
        self.highlight_targets = [self.content_frame]

        # Add option buttons in sidebar
        self.display_options()
        self.show_home()
    
    # Displays home screen in content frame
    def show_home(self):
        self.clear_content()
        self.welcome_label = ctk.CTkLabel(
            self.content_frame, 
            text=f"Welcome to {self.restaurant_data['name']}!",
            font=("Arial", 20)
        )
        self.welcome_label.pack(pady=20)
        self.highlight_targets = [self.content_frame]
   
    # Displays options in sidebar
    def display_options(self):
        for option in self.options_menu.options:
            button = ctk.CTkButton(
                self.sidebar,
                text=option["title"],
                command=lambda opt=option: self.handle_option(opt)
            )
            button.pack(pady=5, padx=10, fill="x")
   
    # Cleans content in content frame when changing options
    def clear_content(self):
        """Remove everything from the content frame."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
   
    # Conditional runs after taking in user's chosen option
    def handle_option(self, option):
        menu_categories = self.restaurant_data["menu"]

        if option["id"] == 1:  # View Menu
            self.show_menu(menu_categories)

        elif option["id"] == 2:  # Add Item
            self.show_add_item_form(menu_categories)

        elif option["id"] == 3:
            self.show_remove_item_form(menu_categories)

        elif option["id"] == 4:  # Save Data
            save_data(self.file_path, self.restaurant_data)
            self.highlight_targets_frame()

        elif option["id"] == 5:  # Exit
            close_program()
  
    # Highlights targeted frames when executing save to JSON
    def highlight_targets_frame(self, color="light green", duration=100):
        original_colors = []
        for target in self.highlight_targets:
            if isinstance(target, ctk.CTkCanvas):
                original_colors.append(target.cget("bg"))
                target.configure(bg=color)
            else:
                original_colors.append(target.cget("fg_color"))
                target.configure(fg_color=color)

        def reset_colors():
            for target, orig in zip(self.highlight_targets, original_colors):
                if isinstance(target, ctk.CTkCanvas):
                    target.configure(bg=orig)
                else:
                    target.configure(fg_color=orig)

        self.root.after(duration, reset_colors)

    # Option 1: Show Menu Function
    def show_menu(self, menu_categories):
        self.clear_content()
        # Title at top
        title = ctk.CTkLabel(
            self.content_frame,
            text=self.restaurant_data["name"],
            font=("Arial", 18)
        )
        title.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=0)

        # Scrollable canvas inside content_frame
        canvas = ctk.CTkCanvas(
            self.content_frame,
            bg="light blue",
            highlightthickness=0
        )
        scrollbar = ctk.CTkScrollbar(
            self.content_frame,
            orientation="vertical",
            command=canvas.yview
        )
        scroll_frame = ctk.CTkFrame(
            canvas,
            fg_color="light blue",
            corner_radius=0,
            border_width=0
        )  # match canvas color

        # Bind frame configure to update canvas scrollregion
        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Add scroll_frame to canvas
        scroll_frame_window = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        self.highlight_targets = [canvas, scroll_frame]

        # Make scroll_frame width track canvas width on resize
        def resize_scroll_frame(event):
            canvas.itemconfig(scroll_frame_window, width=event.width)

        canvas.bind("<Configure>", resize_scroll_frame)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Place canvas and scrollbar in grid
        canvas.grid(row=1, column=0, sticky="nsew")
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.content_frame.grid_rowconfigure(1, weight=1)

        # Populate menu categories and items
        for category in menu_categories:
            cat_label = ctk.CTkLabel(scroll_frame, text=category["category"], font=("Arial", 16, "bold"))
            cat_label.pack(pady=5)

            for item in category["items"]:
                text = f"{item['name']} - ${item['price']:.2f} "
                if not item['in_stock']:
                    text += "(Out of stock)"
                item_label = ctk.CTkLabel(scroll_frame, text=text, anchor="w", justify="left")
                item_label.pack(padx=20)

    # Option 2: Show Add Item Form Function
    def show_add_item_form(self, menu_categories):
        self.clear_content()

        title = ctk.CTkLabel(self.content_frame, text="Add Menu Item", font=("Arial", 18))
        title.pack(pady=10)

        # Category dropdown
        categories = [cat["category"] for cat in menu_categories]
        self.category_var = ctk.StringVar(value=categories[0])

        cat_dropdown = ctk.CTkOptionMenu(
            self.content_frame, 
            values=categories, 
            variable=self.category_var
        )
        cat_dropdown.pack(pady=5)

        # Item name
        self.item_name_entry = ctk.CTkEntry(self.content_frame, placeholder_text="Item name")
        self.item_name_entry.pack(pady=5)

        # Item price
        self.item_price_entry = ctk.CTkEntry(self.content_frame, placeholder_text="Item price")
        self.item_price_entry.pack(pady=5)

        # Submit button
        submit_btn = ctk.CTkButton(
            self.content_frame, 
            text="Add Item", 
            command=lambda: self.add_item_to_category(menu_categories)
        )
        submit_btn.pack(pady=10)
        self.highlight_targets = [self.content_frame]

    # Option 2: Execute Add Item Function when Form Data is Given
    def add_item_to_category(self, menu_categories):
        category_name = self.category_var.get()
        new_item_name = self.item_name_entry.get()
        try:
            new_item_price = float(self.item_price_entry.get())
        except ValueError:
            error_label = ctk.CTkLabel(
                self.content_frame, 
                text="Invalid price. Enter a number.", 
                text_color="red"
            )
            error_label.pack()
            self.content_frame.after(2000, error_label.destroy)
            return

        for category in menu_categories:
            if category["category"] == category_name:
                category_items = category["items"]
                new_id = category_items[-1]["id"] + 1 if category_items else 1
                category_items.append({
                    "id": new_id,
                    "name": new_item_name,
                    "price": new_item_price,
                    "in_stock": True
                })
                break

        confirm_label = ctk.CTkLabel(
            self.content_frame, 
            text=f"{new_item_name} added successfully!", 
            text_color="green"
        )
        confirm_label.pack()

        # Automatically remove confirmation after 1.5 seconds
        self.content_frame.after(1500, confirm_label.destroy)

        # Update IDs
        update_ids(menu_categories)

    # Option 3: Show Remove Item Form Function
    def show_remove_item_form(self, menu_categories):
        self.clear_content()

        # Adding text header component
        self.title = ctk.CTkLabel(self.content_frame, text="Remove Menu Item", font=("Arial", 18))
        self.title.pack(pady=10)

        # Item name
        self.item_name_entry = ctk.CTkEntry(self.content_frame, placeholder_text="Item To Be Removed")
        self.item_name_entry.pack(pady=5)

        # Submit button
        submit_btn = ctk.CTkButton(
            self.content_frame, 
            text="Remove Item", 
            command=lambda: self.remove_item(menu_categories)
        )
        submit_btn.pack(pady=10)

    def remove_item(self, menu_categories):
        self.item_to_be_removed = self.item_name_entry.get()
        found = False

        for category in self.restaurant_data["menu"]:
            for item in category["items"]:
                if self.item_to_be_removed.strip().lower() == item["name"].strip().lower():
                    category["items"].remove(item)
                    found = True
                    break
            if found:
                break

        if found:
            confirm_label = ctk.CTkLabel(
                self.content_frame, 
                text=f"{self.item_to_be_removed} removed successfully!", 
                text_color="green"
            )
            confirm_label.pack()
            self.content_frame.after(1500, confirm_label.destroy)
            # Update IDs after removal
            update_ids(self.restaurant_data["menu"])

        else:
            error_label = ctk.CTkLabel(
                self.content_frame, 
                text="Item not found", 
                text_color="red"
            )
            error_label.pack()
            self.content_frame.after(2000, error_label.destroy)

if __name__ == "__main__":
    file_path = "data/restaurant_data.json"

    ctk.set_appearance_mode("System")  
    ctk.set_default_color_theme("blue")  

    root = ctk.CTk()
    app = Restaurant_GUI(root, file_path)
    root.mainloop()