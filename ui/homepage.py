import tkinter as tk

class HomePage(tk.Frame):
    def __init__(self, parent, controller) -> None:
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Homepage title
        title = tk.Label(self, 
                         text="Welcome to Janki!", 
                         font=("Arial", 30, "bold"),
                         pady=20)
        title.pack()
        
        # Review button
        reviews_button = tk.Button(self, 
                                   text="Reviews", 
                                   command= lambda: self.start_reviews())
        reviews_button.pack()
        
        # Add new cards button
        add_card_button = tk.Button(self,
                                    text="Add new cards",
                                    command= lambda: controller.show_frame("AddCardsPage"))
        add_card_button.pack()
        
        # Quit button
        quit_button = tk.Button(self,
                                text="Quit",
                                command= lambda: controller.quit_app())
        quit_button.pack()
        
    def start_reviews(self):
        
        self.controller.show_frame("ReviewPage")