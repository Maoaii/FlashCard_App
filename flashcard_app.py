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

AVAILABLE_FRAMES = (HomePage, ReviewPage, AddCardsPage)
APP_NAME: str = "Flashcard App"
DATA_PATH: str = "./data/data.json"
READING_REVIEW = "reading"
MEANING_REVIEW = "meaning"

class FlashcardApp(tk.Tk):
    def __init__(self, *args, **kwargs) -> None:
        # TODO: will be using this for the reviews.
        # TODO: change this to a dictionary
        today = date.today()
        self.today_string = today.strftime("%x")
        self.levels = {
            1: (today + datetime.timedelta(days=1)).strftime("%x"),
            2: (today + datetime.timedelta(days=3)).strftime("%x"),
            3: (today + datetime.timedelta(days=7)).strftime("%x"),
            4: (today + datetime.timedelta(days=14)).strftime("%x"),
            5: (today + datetime.timedelta(days=31)).strftime("%x"),
        }
        
        # Seed the random generator
        random.seed()
        
        # Set up current cards
        self.current_review: Dict[CardReview] = []
        self.current_card_review: CardReview = None
        self.start_new_review()
        
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
        
        if page_name == ReviewPage.__name__:
            self.start_new_review()
            
            if self.current_review == []:
                self.show_frame(HomePage.__name__)
                messagebox.showinfo("No cards to review", "You have no cards to review today.")
                return
            
            frame.start_review()
    
    
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
            "next_review": self.levels.get(1), # ! This is a timestamp for the next review
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
        # Create a copy of all the cards up for review
        with open(DATA_PATH, "r") as data_file:
            all_cards = json.load(data_file)["cards"]
        
        # Create reviews for readings and for meanings
        for card in all_cards:
            # If the card is up for review, create a review for it
            if card.get("next_review") == self.today_string:
                self.current_review.append(
                    CardReview(card.get("title"), card.get(READING_REVIEW), READING_REVIEW))
                self.current_review.append(
                    CardReview(card.get("title"), card.get(MEANING_REVIEW), MEANING_REVIEW))
        
        try:
            self.setup_card()
        except IndexError:
            # TODO: Gotta figure something out here (when there are no cards to review)
            pass
    
        
    def setup_card(self):
        self.current_card_review = random.choice(self.current_review)
    
    
    def submit_answer(self, answer):
        if not answer:
            raise MissingInfoError()
        
        if not self.check_answer(answer):
            # Setup new card
            self.setup_card()
            
            raise WrongAnswerError()
        
        # Remove card from deck
        self.current_review.remove(self.current_card_review)
        
        # Setup new card
        self.setup_card()
        
    
    def check_answer(self, answer: str) -> bool:
        return answer.casefold() in self.current_card_review.answer.casefold()
    
    
    def get_current_review(self) -> CardReview:
        return self.current_card_review

    # TODO: Implement this
    def update_card_levels(self):
        # Load reviews in file
        
        # Check which reviews in current review were answered correctly
        
        # Find the corresponding reviews in the file and update their levels
        
        pass
    
    
    def quit_app(self):
        self.quit()
