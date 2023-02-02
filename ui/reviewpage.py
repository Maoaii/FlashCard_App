import tkinter as tk
from tkinter import messagebox
from exceptions.WrongAnswerError import WrongAnswerError
from exceptions.MissingInfoError import MissingInfoError

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
        self.card_title_label = tk.Label(self,
                                    text= "XXX",
                                    pady=20)
        self.card_title_label.pack()
        
        # Card review type
        self.card_review_type_label = tk.Label(self, text="XXX")
        self.card_review_type_label.pack()
        
        # Card answer setup
        card_answer_entry = tk.Entry(self)
        card_answer_entry.pack()
        
        # Submit answer button
        add_card_button = tk.Button(self, text="Submit answer",
                                    command= lambda: self.submit_answer(card_answer_entry.get()))
        add_card_button.pack()
        
        # Back button
        back_button = tk.Button(self,
                                text="Back",
                                command= lambda: self.back_button_clicked())
        back_button.pack()
    
    def start_review(self):
        # Set up current card
        self.current_card_review = self.controller.get_current_review()
        
        # Set up labels
        self.card_title_label.config(text=self.current_card_review.get_question())
        self.card_review_type_label.config(text=self.current_card_review.get_review_type())
    
    
    def submit_answer(self, answer):
        try:
            self.controller.submit_answer(answer)
        except IndexError:
            messagebox.showerror(title="All answered correctly!", message="All answered correctly!")
            self.back_button_clicked()
        except MissingInfoError:
            messagebox.showerror(title="Please fill out all the entries", message="Please fill out all the entries")
        except WrongAnswerError:
            messagebox.showerror(title="Wrong answer.", message=f"Wrong answer. Correct answer: {self.current_card_review.get_answer()}") 
        else:
            messagebox.showinfo(title="Correct answer!", message="Correct answer")
        finally:
            self.clear_entries()
            self.current_card_review = self.controller.get_current_review()
            self.card_title_label.config(text=self.current_card_review.get_question())
            self.card_review_type_label.config(text=self.current_card_review.get_review_type())
            
        
    
    def back_button_clicked(self):
        self.clear_entries()
        self.controller.update_card_levels()
        self.controller.show_frame("HomePage")
        
        
    def clear_entries(self):
        for entry in self.winfo_children():
            if isinstance(entry, tk.Entry):
                entry.delete(0, "end")
    
    