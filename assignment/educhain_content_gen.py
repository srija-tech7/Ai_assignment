from educhain.content import MCQGenerator, LessonPlanner  

def generate_mcqs(topic):
    generator = MCQGenerator()
    questions = generator.generate(topic, num_questions=5)
    return questions

def generate_lesson_plan(subject):
    planner = LessonPlanner()
    lesson = planner.create(subject)
    return lesson
