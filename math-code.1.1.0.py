import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

quiz = [
    {"image": "rectangle.png", "question": "What is the area of a 10 × 5 rectangle?", "answer": "50"},
    {"image": "triangle.png", "question": "What is the area of a triangle with base 10 and height 4?", "answer": "20"},
    {"image": "circle.png", "question": "What is the area of a circle with radius 3? (Use 3.14)", "answer": "28.26"}
]

question_no = 0
students_score = 0

root = tk.Tk()
root.title("Simple 3-Question Math Quiz")
root.geometry("600x500")

menu_frame = tk.Frame(root)
menu_frame.pack()

tk.Label(menu_frame, text="Welcome to the Math Quiz!", font=("Arial", 16)).pack(pady=10)
tk.Label(menu_frame, text="Enter your name:", font=("Arial", 12)).pack()
name_entry = tk.Entry(menu_frame, font=("Arial", 12))
name_entry.pack(pady=5)
tk.Label(menu_frame, text="Select difficulty:", font=("Arial", 12)).pack()

def start_quiz(difficulty):
    student_name = name_entry.get().strip()
    if student_name == "":
        messagebox.showwarning("Input Error", "Please enter your name.")
        return
    print(f"Selected difficulty: {difficulty}")  # Just for demonstration/logging
    menu_frame.pack_forget()
    quiz_frame.pack()
    show_question()

tk.Button(menu_frame, text="Easy", command=lambda: start_quiz("Easy"), font=("Arial", 12)).pack(pady=2)
tk.Button(menu_frame, text="Medium", command=lambda: start_quiz("Medium"), font=("Arial", 12)).pack(pady=2)
tk.Button(menu_frame, text="Hard", command=lambda: start_quiz("Hard"), font=("Arial", 12)).pack(pady=2)

def show_question():
    question_data = quiz[question_no]
    question_label.config(text=question_data["question"])
    try:
        img = Image.open(question_data["image"])
        img = img.resize((300, 200))
        photo = ImageTk.PhotoImage(img)
        image_label.config(image=photo)
        image_label.image = photo
    except FileNotFoundError:
        image_label.config(text="Image not found", image='')

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
        messagebox.showinfo("Incorrect", f"❌ The correct answer was {correct}")

    question_no += 1

    if question_no < len(quiz):
        show_question()
    else:
        messagebox.showinfo("Quiz Over", f"You scored {students_score} out of {len(quiz)}")
        root.destroy()

quiz_frame = tk.Frame(root)

question_label = tk.Label(quiz_frame, text="", font=("Arial", 14))
question_label.pack(pady=10)

image_label = tk.Label(quiz_frame)
image_label.pack(pady=10)

answer_entry = tk.Entry(quiz_frame, font=("Arial", 14))
answer_entry.pack(pady=10)

submit_button = tk.Button(quiz_frame, text="Submit Answer", command=check_answer)
submit_button.pack(pady=10)

root.mainloop()
