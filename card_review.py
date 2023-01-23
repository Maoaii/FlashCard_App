class CardReview():
    def __init__(self, question, answer, review_type) -> None:
        self.question = question
        self.answer = answer
        self.review_type = review_type
    
    def get_question(self):
        return self.question
    
    def get_answer(self):
        return self.answer
    
    def get_review_type(self):
        return self.review_type
    
    