import json
import random
import tkinter as tk
import datetime
from tkinter import messagebox
from datetime import date
from typing import Dict
from exceptions.CardAlreadyExistsError import CardAlreadyExistsError
from exceptions.MissingInfoError import MissingInfoError
from exceptions.WrongAnswerError import WrongAnswerError
from tkinter import font as tkfont
from ui.homepage import HomePage
from ui.reviewpage import ReviewPage
from ui.addcardspage import AddCardsPage
from card_review import CardReview

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 500

AVAILABLE_FRAMES = (HomePage, ReviewPage, AddCardsPage)
APP_NAME: str = "Janki"
DATA_PATH: str = "./data/data.json"
READING_REVIEW = "reading"
MEANING_REVIEW = "meaning"

today = date.today()
TODAY_STRING = today.strftime("%x")
LEVELS = {
    1: (today + datetime.timedelta(days=1)).strftime("%x"),
    2: (today + datetime.timedelta(days=3)).strftime("%x"),
    3: (today + datetime.timedelta(days=7)).strftime("%x"),
    4: (today + datetime.timedelta(days=14)).strftime("%x"),
    5: (today + datetime.timedelta(days=31)).strftime("%x"),
}

class FlashcardApp(tk.Tk):
    def __init__(self, *args, **kwargs) -> None:
        
        # Seed the random generator
        random.seed()
        
        self.window = tk.Tk.__init__(self, *args, **kwargs)
        
        # Setting up the window
        self.title(APP_NAME)
        self.config(padx=50, pady=30)
        self.resizable(False, False)
        self.center_window()
        
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
        
        if page_name == ReviewPage.__name__:
            self.start_new_review()
            
            if self.current_reviews == []:
                self.show_frame(HomePage.__name__)
                messagebox.showinfo("No cards to review", "You have no cards to review today.")
                return
            
            frame.start_review()

    
    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        x = (screen_width / 2) - (SCREEN_WIDTH / 2)
        y = (screen_height / 2) - (SCREEN_HEIGHT / 2)
        
        self.geometry("%dx%d+%d+%d" % (SCREEN_WIDTH, SCREEN_HEIGHT, x, y))
        
    
    
    def add_card(self, card_title, card_reading, card_meaning, card_type):
        if not card_title or not card_reading or not card_meaning or not card_type:
            raise MissingInfoError()
        if self.card_already_exists(card_title):
            raise CardAlreadyExistsError()
        
        # Create a dict with the info and encode it into json
        card = {
            "title": card_title, 
            "type": card_type,
            "reading": card_reading,
            "meaning": card_meaning,
            "level": 1,
            "next_review": LEVELS.get(1), # ! This is a timestamp for the next review
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
            if card_title in card.get("title"):
                return True
        
        return False

    
    def start_new_review(self):
        self.current_reviews: Dict[CardReview] = []
        self.answered_reviews: Dict[CardReview] = []
        self.current_card_review: CardReview = None
        
        # Create a copy of all the cards up for review
        with open(DATA_PATH, "r") as data_file:
            all_cards = json.load(data_file)["cards"]
        
        # Create reviews for readings and for meanings
        for card in all_cards:
            # If the card is up for review, create a review for it
            if card.get("next_review") == TODAY_STRING:
                self.current_reviews.append(CardReview(card.get("title"), card.get("reading"), card.get("meaning")))
        
        if all_cards == [] or self.current_reviews == []:
            return
        
        
        self.setup_card()
    
        
    def setup_card(self):
        self.current_card_review = random.choice(self.current_reviews)
    
    
    def submit_answer(self, answer):
        if not answer:
            raise MissingInfoError()
        
        if not self.answered_correctly(answer):
            # Update card missed
            self.current_card_review.missed()
            
            # Setup new card
            self.setup_card()
            
            raise WrongAnswerError()
        
        # Remove card from deck
        self.current_card_review.answered_correctly()
        if self.current_card_review.review_done():
            self.current_reviews.remove(self.current_card_review)
            self.answered_reviews.append(self.current_card_review)
        
        # Setup new card
        self.setup_card()
        
    
    def answered_correctly(self, answer: str) -> bool:
        return answer.casefold() in self.current_card_review.get_answer().casefold()
    
    
    def get_current_review(self) -> CardReview:
        return self.current_card_review


    def update_card_levels(self):
        with open(DATA_PATH, "r") as data_file:
            data = json.load(data_file)

        
        for card in self.answered_reviews:
            if card.has_missed_review():
                # level down the card
                self.level_down_card(card.get_question(), data["cards"])
            else:
                # level up the card
                self.level_up_card(card.get_question(), data["cards"])
            
        
        self.update_data_file(data)
    
    
    def level_up_card(self, card_title, all_cards):
        for card in all_cards:
            if card["title"] == card_title:
                card["level"] += 1
                if card["level"] > 5:
                    card["level"] = 5
                card["next_review"] = LEVELS.get(card["level"])
    
    
    def level_down_card(self, card_title, all_cards):
        for card in all_cards:
            if card["title"] == card_title:
                card["level"] -= 1
                if card["level"] < 1:
                    card["level"] = 1
                card["next_review"] = LEVELS.get(card["level"])
    
    
    def update_data_file(self, data):
        with open(DATA_PATH, "w") as data_file:
            json_string = json.dumps(data, ensure_ascii=False, indent=4)
            data_file.write(json_string)
            

    def quit_app(self):
        self.quit()
