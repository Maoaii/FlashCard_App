from random import choice

REVIEW_TYPES = ["reading", "meaning"]

class CardReview():
    def __init__(self, question, reading, meaning) -> None:
        self.question = question
        self.answer = {
            "reading": reading,
            "meaning": meaning,
        }
        self.missed_review = False
        self.answered_reading_correctly = False
        self.answered_meaning_correctly = False
    
    def get_question(self):
        return self.question
    
    def get_answer(self):
        return self.answer.get(self.review_type)
    
    def get_review_type(self):
        if not self.answered_reading_correctly and not self.answered_meaning_correctly:
            self.review_type = choice(REVIEW_TYPES)
        else:
            self.review_type = "reading" if not self.answered_reading_correctly else "meaning"

        return self.review_type
    
    def has_missed_review(self):
        return self.missed_review

    def answered_correctly(self):
        if self.review_type == "reading":
            self.answered_reading_correctly = True
        else:
            self.answered_meaning_correctly = True
    
    def missed(self):
        self.missed_review = True
    
    def review_done(self) -> bool:
        return self.answered_reading_correctly and self.answered_meaning_correctly
        
        

    
    