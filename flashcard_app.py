import json
import tkinter as tk
from exceptions.CardAlreadyExistsError import CardAlreadyExistsError
from exceptions.MissingInfoError import MissingInfoError
from tkinter import font as tkfont
from ui.homepage import HomePage
from ui.reviewpage import ReviewPage
from ui.addcardspage import AddCardsPage

AVAILABLE_FRAMES = (HomePage, ReviewPage, AddCardsPage)
APP_NAME: str = "Flashcard App"
DATA_PATH: str = "./data/data.json"

class FlashcardApp(tk.Tk):
    
    
    
    def __init__(self, *args, **kwargs) -> None:
        self.window = tk.Tk.__init__(self, *args, **kwargs)
        
        # Setting up the window
        self.title(APP_NAME)
        self.config(padx=50, pady=30)
        
        # Create a container for all the frames
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        # Populate frames available
        self.frames = {}
        for F in AVAILABLE_FRAMES:
            frame_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[frame_name] = frame
            
            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(HomePage.__name__)
        
    def show_frame(self, page_name):
        # Raise the frame we want to the front
        frame = self.frames[page_name]
        frame.tkraise()
    
    def add_card(self, card_title, card_reading, card_meaning, card_type):
        if not card_title or not card_reading or not card_meaning or not card_type:
            raise MissingInfoError()
        if self.card_already_exists(card_title):
            raise CardAlreadyExistsError()
        
        # Create a dict with the info and encode it into json
        card = {
            card_title: {    
                "type": card_type,
                "reading": card_reading,
                "meaning": card_meaning,
                "level": 1,
            }
        }
        
        # Read the data content so I can overwrite it with new info
        with open(DATA_PATH, "r") as data_file:
            data = json.load(data_file)
            data["cards"].append(card)
        
        # Overwrite the data file with the new info
        with open(DATA_PATH, "w") as data_file:
            json_string = json.dumps(data, ensure_ascii=False, indent=4)
            data_file.write(json_string)
    
    def card_already_exists(self, card_title) -> bool:
        with open(DATA_PATH, "r") as data_file:
            data = json.load(data_file)
        
        for card in data["cards"]:
            if card_title in card:
                return True
        
        return False
    
    def check_answer(self, card, answer) -> bool:
        pass 
    
    def get_card(self) -> dict:
        pass
    
    def quit_app(self):
        self.quit()
