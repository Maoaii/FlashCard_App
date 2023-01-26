class CardReview():
    def __init__(self, question, answer, review_type) -> None:
        self.question = question
        self.answer = answer
        self.review_type = review_type
        self.answered_correctly = True
    
    def get_question(self):
        return self.question
    
    def get_answer(self):
        return self.answer
    
    def get_review_type(self):
        return self.review_type
    
    def answered_correctly(self):
        self.answered_correctly = True
    
    def get_answered_correctly(self):
        return self.answered_correctly
    
    