import tkinter as tk
from tkinter import messagebox
from exceptions.WrongAnswerError import WrongAnswerError

class ReviewPage(tk.Frame):
    def __init__(self, parent, controller) -> None:
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Reviews title
        title = tk.Label(self, 
                         text="Reviews", 
                         font=("Arial", 30, "bold"),
                         pady=20)
        title.pack()
        
        # Card title setup
        card_title_label = tk.Label(self,
                                    text=self.controller.get_card(),
                                    pady=20)
        card_title_label.pack()
        
        # Card answer setup
        card_answer_entry = tk.Entry(self)
        card_answer_entry.pack()
        
        # Submit answer button
        add_card_button = tk.Button(self, text="Submit answer",
                                    command= lambda: self.submit_answer())
        add_card_button.pack()
        
        # Back button
        back_button = tk.Button(self,
                                text="Back",
                                command= lambda: controller.show_frame("HomePage"))
        back_button.pack()
    
    
    def submit_answer(self):
        try:
            self.controller.submit_answer(self.card_answer_entry.get())
        except WrongAnswerError:
            messagebox.showerror(title="Wrong answer", message="Wrong answer")