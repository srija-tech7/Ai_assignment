class MCQGenerator:
    def generate(self, topic, num_questions=5):
        return [f"MCQ {i+1} on {topic}" for i in range(num_questions)]

class LessonPlanner:
    def create(self, subject):
        return {
            "subject": subject,
            "objectives": ["Understand key concepts", "Apply to real-world problems"],
            "activities": ["Lecture", "Practice", "Quiz"]
        }