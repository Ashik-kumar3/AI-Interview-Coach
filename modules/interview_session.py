class InterviewSession:

    def __init__(self):

        self.results = []

    def add_result(
        self,
        question,
        answer,
        answer_score,
        keywords_found,
        missing_keywords,
        feedback,
        llm_result=None
    ):

        self.results.append({

            "question": question,

            "answer": answer,

            "answer_score": answer_score,

            "keywords_found": keywords_found,

            "missing_keywords": missing_keywords,

            "feedback": feedback,

            "llm_result": llm_result

        })

    def get_results(self):

        return self.results