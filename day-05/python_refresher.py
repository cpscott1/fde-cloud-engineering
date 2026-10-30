class StudentQuestion:
    def __init__(self, question, student_name, grade):
        self.question = question
        self.student_name = student_name
        self.grade = grade
        
    def to_dict(self):
        return {
            "question": self.question,
            "student_name": self.student_name,
            "grade": self.grade
        }

question1 = StudentQuestion(
    "What is the attendance policy",
    "Joe",
    "12th"
)


print(question1.to_dict())
