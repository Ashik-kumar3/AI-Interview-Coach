class InterviewManager:

    def __init__(self, questions):

        self.questions = questions

        self.current_index = 0

        self.results = []

    def current_question(self):

        return self.questions[self.current_index]

    def has_next(self):

        return self.current_index < len(self.questions) - 1

    def next_question(self):

        if self.has_next():

            self.current_index += 1

    def question_number(self):

        return self.current_index + 1

    def total_questions(self):

        return len(self.questions)

    def save_result(
        self,
        result
    ):

        self.results.append(result)

    def get_results(self):

        return self.results