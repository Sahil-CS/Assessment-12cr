import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random

def generate_easy_quiz():
    operators = ["+", "-", "*", "/"]
    quiz = []
    for _ in range(3):
        num1 = random.randint(1, 20)
        num2 = random.randint(1, 20)
        op = random.choice(operators)

        if op == "+":
            question = f"What is {num1} + {num2}?"
            answer = str(num1 + num2)
        elif op == "-":
            question = f"What is {num1} - {num2}?"
            answer = str(num1 - num2)
        elif op == "*":
            question = f"What is {num1} × {num2}?"
            answer = str(num1 * num2)
        elif op == "/":
            num1 = num1 * num2
            question = f"What is {num1} ÷ {num2}?"
            answer = str(num1 // num2)

        quiz.append({"question": question, "answer": answer})
    return quiz

medium_quiz = [
    {"image": "rectangle.png", "question": "What is the area of a 10 × 5 rectangle?", "answer": "50"},
    {"image": "triangle.png", "question": "What is the area of a triangle with base 10 and height 4?", "answer": "20"},
    {"image": "circle.png", "question": "What is the area of a circle with radius 3? (Use 3.14)", "answer": "28.26"}
]

hard_quiz = [{"question": "IDK", "answer": ""}]

quiz = []
question_no = 0
students_score = 0

root = tk.Tk()
root.title("Simple Math Quiz")
root.geometry("600x500")

menu_frame = tk.Frame(root)
menu_frame.pack()

title_label = tk.Label(menu_frame, text="Welcome to the Math Quiz!", font=("Arial", 16))
title_label.pack(pady=10)

name_label = tk.Label(menu_frame, text="Enter your name:", font=("Arial", 12))
name_label.pack()

name_entry = tk.Entry(menu_frame, font=("Arial", 12))
name_entry.pack(pady=5)

difficulty_label = tk.Label(menu_frame, text="Select difficulty:", font=("Arial", 12))
difficulty_label.pack()

def start_easy():
    start_quiz("Easy")

def start_medium():
    start_quiz("Medium")

def start_hard():
    start_quiz("Hard")

easy_button = tk.Button(menu_frame, text="Easy", command=start_easy, font=("Arial", 12))
easy_button.pack(pady=2)

medium_button = tk.Button(menu_frame, text="Medium", command=start_medium, font=("Arial", 12))
medium_button.pack(pady=2)

hard_button = tk.Button(menu_frame, text="Hard", command=start_hard, font=("Arial", 12))
hard_button.pack(pady=2)

def quit_quiz():
    if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
        root.destroy()

quit_menu_button = tk.Button(menu_frame, text="Quit", command=quit_quiz, font=("Arial", 12), bg="red", fg="white")
quit_menu_button.pack(pady=10)

quiz_frame = tk.Frame(root)

question_label = tk.Label(quiz_frame, text="", font=("Arial", 14))
question_label.pack(pady=10)

image_label = tk.Label(quiz_frame)
image_label.pack(pady=10)

answer_entry = tk.Entry(quiz_frame, font=("Arial", 14))
answer_entry.pack(pady=10)

submit_button = tk.Button(quiz_frame, text="Submit Answer", font=("Arial", 12), command=lambda: check_answer())
submit_button.pack(pady=10)

quit_quiz_button = tk.Button(quiz_frame, text="Quit", command=quit_quiz, font=("Arial", 12), bg="red", fg="white")
quit_quiz_button.pack(pady=5)

def start_quiz(difficulty):
    global quiz, question_no, students_score

    student_name = name_entry.get().strip()
    if student_name == "":
        messagebox.showwarning("Input Error", "Please enter your name.")
        return

    question_no = 0
    students_score = 0

    if difficulty == "Easy":
        quiz = generate_easy_quiz()
    elif difficulty == "Medium":
        quiz = medium_quiz
    else:
        quiz = hard_quiz

    menu_frame.pack_forget()
    quiz_frame.pack()
    show_question()

def show_question():
    question_data = quiz[question_no]
    question_label.config(text=question_data["question"])

    if "image" in question_data:
        try:
            img = Image.open(question_data["image"])
            img = img.resize((300, 200))
            photo = ImageTk.PhotoImage(img)
            image_label.config(image=photo, text="")
            image_label.image = photo
        except FileNotFoundError:
            image_label.config(text="Image not found", image="")
            image_label.image = None
    else:
        image_label.config(image="", text="")
        image_label.image = None

    answer_entry.delete(0, tk.END)
    answer_entry.focus()

def check_answer():
    global question_no, students_score
    user_answer = answer_entry.get().strip()
    correct = quiz[question_no]["answer"]

    if user_answer == correct:
        students_score += 1
        messagebox.showinfo("Correct", "✅ Well done!")
    else:
        if correct == "":
            messagebox.showinfo("Info", "❓ No correct answer set.")
        else:
            messagebox.showinfo("Incorrect", f"❌ The correct answer was {correct}")

    question_no += 1

    if question_no < len(quiz):
        show_question()
    else:
        messagebox.showinfo("Quiz Over", f"You scored {students_score} out of {len(quiz)}")
        root.destroy()

root.mainloop()
