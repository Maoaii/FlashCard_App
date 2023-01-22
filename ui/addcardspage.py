import tkinter as tk
from tkinter import ttk, messagebox
from exceptions.CardAlreadyExistsError import CardAlreadyExistsError
from exceptions.MissingInfoError import MissingInfoError

class AddCardsPage(tk.Frame):
    def __init__(self, parent, controller) -> None:
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Window title
        title = tk.Label(self, 
                         text="Add new cards to your deck",
                         font=("Arial", 30, "bold"),
                         pady=20)
        title.pack()

        # Set up for card's title
        card_title_label = tk.Label(self, text="Card title")
        card_title_entry = tk.Entry(self, width=22)
        card_title_label.pack(pady=2)
        card_title_entry.pack(pady=5)
        card_title_entry.focus()
        
        # Set up for card's reading
        card_reading_label = tk.Label(self, text="Card reading")
        card_reading_entry = tk.Entry(self, width=22)
        card_reading_label.pack(pady=2)
        card_reading_entry.pack(pady=5)
        
        # Set up for card's meaning
        card_meaning_label = tk.Label(self, text="Card meaning")
        card_meaning_entry = tk.Entry(self, width=22)
        card_meaning_label.pack(pady=2)
        card_meaning_entry.pack(pady=5)
        
        # Set up card type
        card_type_label = tk.Label(self, text="Card type")
        card_type = tk.StringVar()
        card_type_combobox = ttk.Combobox(self, textvariable=card_type)
        card_type_combobox.config(values=('Kanji', 'Vocabulary'),
                                  state="readonly", width=20)
        card_type_label.pack(pady=2)
        card_type_combobox.pack(pady=5)
        
        # Add card button
        add_card_button = tk.Button(self,
                                    text="Add card",
                                    width=10,
                                    command= lambda: self.add_new_card(card_title_entry.get(),
                                                                         card_reading_entry.get(),
                                                                         card_meaning_entry.get(),
                                                                         card_type.get()))
        add_card_button.pack(pady=10)
        
        # Back button
        back_button = tk.Button(self,
                                text="Back",
                                command= lambda: controller.show_frame("HomePage"))
        back_button.pack(pady=2)
    
    def add_new_card(self, card_title, card_reading, card_meaning, card_type):
        try:
            self.controller.add_card(card_title, card_reading, card_meaning, card_type)
        except MissingInfoError:
            messagebox.showerror(title="Please fill out all the entries", message="Please fill out all the entries")
        except CardAlreadyExistsError:
            messagebox.showerror(title="Card already exists", message="Card already exists")
        else:
            messagebox.showinfo(title="Card added succesfully!", message="Card added succesfully!")
        
        