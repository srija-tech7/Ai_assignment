import requests

# Replace this with the port your server is running on if different
BASE_URL = "http://localhost:5000"

# Test 1: Generate MCQs
mcq = requests.post(f"{BASE_URL}/tool/generate_mcqs", json={"topic": "Python functions"})
print("📘 MCQ Response:\n", mcq.json())

# Test 2: Lesson Plan
lesson = requests.post(f"{BASE_URL}/resource/lesson_plan", json={"subject": "algebra"})
print("\n📗 Lesson Plan Response:\n", lesson.json())

# Test 3: Flashcards
flashcards = requests.post(f"{BASE_URL}/tool/flashcards", json={"subject": "OOP"})
print("\n📕 Flashcards Response:\n", flashcards.json())
