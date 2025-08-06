# Author: Sahil Vagh
# Date: 25/07/2025

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
from tkinter import font 
from datetime import datetime

# Fonts and button size settings.
title_font = ("Forte", 25)
big_font = ("Century", 14)
normal_font = ("Courier New", 12)
button_width = 17

# Global variables to keep track of quiz info.
questions = []
user_answers = []
current_question = 0
score = 0
player_name = ""
question_stack = []  # Stack to save previous question numbers.

# Check if name has only letters.
def valid_name(name):
    return name.isalpha()

# Check easy answers are numbers from -500 to 500.
def validate_easy_answer(answer):
    try:
        num = float(answer)
        return -500 <= num <= 500
    except ValueError:
        return False

# Check medium answers are numbers from -500 to 500).
def validate_medium_answer(answer):
    try:
        num = float(answer)
        return -500 <= num <= 500
    except ValueError:
        return False

# Check hard answers only have allowed math characters.
def validate_hard_answer(answer):
    if not answer.strip(): 
        return False
    allowed_characters = set("0123456789x^+-*/ ")
    return all(char in allowed_characters for char in answer)

# Make 10 easy questions with +, -, ×, ÷.
def make_easy_questions():
    quiz = []
    for i in range(10):
        a = random.randint(1, 20)
        b = random.randint(1, 20)
        op = random.choice(["+", "-", "*", "/"])
        if op == "+":
            q = f"what is {a} + {b}?"
            ans = str(a + b)
        elif op == "-":
            q = f"what is {a} - {b}?"
            ans = str(a - b)
        elif op == "*":
            q = f"what is {a} × {b}?"
            ans = str(a * b)
        else:
            a = a * b
            q = f"what is {a} ÷ {b}?"
            ans = str(a // b)
        quiz.append({"question": q, "answer": ans, "validator": validate_easy_answer})
    return quiz

# List of medium questions with images and answers.
def make_medium_questions():
    medium_questions = [
        {"image": "rect10x5.png", "question": "area of this rectangle?", "answer": "50"},
        {"image": "tri10x4.png", "question": "area of this triangle?", "answer": "20"},
        {"image": "circle3.png", "question": "area of this circle (use 3.14)", "answer": "28.26"},
        {"image": "rect8x7.png", "question": "area of this rectangle?", "answer": "56"},
        {"image": "tri12x5.png", "question": "area of this triangle?", "answer": "30"},
        {"image": "circle5.png", "question": "area of this circle (use 3.14)", "answer": "78.5"},
        {"image": "rect9x6.png", "question": "area of this rectangle?", "answer": "54"},
        {"image": "tri15x6.png", "question": "area of this triangle?", "answer": "45"},
        {"image": "circle4.png", "question": "area of this circle (use 3.14)", "answer": "50.24"},
        {"image": "rect20x10.png", "question": "area of this rectangle?", "answer": "200"}
    ]
    for q in medium_questions:
        q["validator"] = validate_medium_answer
    return medium_questions

# List of hard questions about differentiation.
def make_hard_questions():
    questions = [
        {"expr": "3x^2", "answer": "6x"},
        {"expr": "5x^3", "answer": "15x^2"},
        {"expr": "2x^2 + 4x", "answer": "4x + 4"},
        {"expr": "7x", "answer": "7"},
        {"expr": "4x^3 + x^2", "answer": "12x^2 + 2x"},
        {"expr": "10x^4", "answer": "40x^3"},
        {"expr": "x^2 + x", "answer": "2x + 1"},
        {"expr": "6x^3 + 3x", "answer": "18x^2 + 3"},
        {"expr": "x^4", "answer": "4x^3"},
        {"expr": "2x^2 + 5", "answer": "4x"}
    ]
    hard_questions = []
    for p in questions:
        hard_questions.append({"question": f"differentiate: {p['expr']}", "answer": p["answer"], "validator": validate_hard_answer})
    return hard_questions

# Start the quiz after checking the name and difficulty.
def start_quiz():
    global questions, current_question, score, player_name, user_answers, question_stack
    name = name_input.get().strip()
    if name == "":
        messagebox.showwarning("error", "please type your name!")
        return
    if not valid_name(name):
        messagebox.showwarning("error", "name can only have letters!")
        return
    player_name = name
    score = 0
    current_question = 0
    user_answers = []
    question_stack = []

    # New: set difficulty title
    if difficulty.get() == "easy":
        questions = make_easy_questions()
        difficulty_title.config(text="Easy Mode")
    elif difficulty.get() == "medium":
        questions = make_medium_questions()
        difficulty_title.config(text="Medium Mode")
    else:
        questions = make_hard_questions()
        difficulty_title.config(text="Hard Mode")

    menu_frame.pack_forget()
    quiz_frame.pack()
    show_question()

# Show the current question and picture if it has one.
def show_question():
    q = questions[current_question]
    question_text.config(text=q["question"])
    if "image" in q:
        try:
            img = Image.open(q["image"])
            img = img.resize((150, 100))
            img_tk = ImageTk.PhotoImage(img)
            image_box.config(image=img_tk)
            image_box.image = img_tk
        except IOError:
            image_box.config(image="", text="Image not found!")
    else:
        image_box.config(image="", text="")
    answer_input.delete(0, tk.END)
    answer_input.focus()

# Check answer, update score, and move to next question.
def submit_answer():
    global current_question, score
    ans = answer_input.get().strip()
    
    validator = questions[current_question].get("validator", lambda x: True)
    if not validator(ans):
        messagebox.showwarning("Invalid Input", 
                             "Easy: Whole numbers -500 to 500\n"
                             "Medium: Numbers -500 to 500\n"
                             "Hard: Only numbers, x, and ^ allowed")
        return
    
    user_answers.append(ans)
    question_stack.append(current_question)
    if ans == questions[current_question]["answer"]:
        score += 1
    current_question += 1
    if current_question < len(questions):
        show_question()
    else:
        end_quiz()

# Go back to the previous question.
def go_back():
    global current_question, score
    if question_stack:
        current_question = question_stack.pop()
        if user_answers:
            last_answer = user_answers.pop()
            if last_answer == questions[current_question]["answer"]:
                score -= 1
        show_question()
    else:
        messagebox.showinfo("Back", "This is the first question.")

# Finish quiz and show score.
def end_quiz():
    save_results_to_file()
    messagebox.showinfo("quiz finished", f"{player_name}, your score is {score}/{len(questions)}, your results are saved in README.txt file.")
    back_to_menu()

# Save the quiz results to a text file.
def save_results_to_file():
    time_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open("README.txt", "a") as file:
        file.write("\n==== MATH QUIZ RESULTS ====\n\n")
        file.write(f"quiz date: {time_now}\n")
        file.write(f"player name: {player_name}\n")
        file.write(f"score: {score}/{len(questions)}\n")
        file.write("===========================\n\n")
        for i in range(len(questions)):
            file.write(f"q{i+1}: {questions[i]['question']}\n")
            file.write(f"your answer: {user_answers[i]}\n")
            file.write(f"correct answer: {questions[i]['answer']}\n")
            file.write("---------------------------\n")

# Close the quiz program.
def quit_game():
    app.destroy()

# Return to the main menu screen.
def back_to_menu():
    quiz_frame.pack_forget()
    menu_frame.pack()

# New: View quiz history from README.txt
def view_history():
    history_win = tk.Toplevel()
    history_win.title("Quiz History")
    history_win.geometry("500x520")
    history_win.config(bg="#ccf2cc")

    title_label = tk.Label(history_win, text="Quiz History", font=title_font, bg="#ccf2cc")
    title_label.pack(pady=(10, 5))

    # Buttons at the top
    button_frame = tk.Frame(history_win, bg="#ccf2cc")
    button_frame.pack(pady=5)

    def clear_text():
        text_area.config(state=tk.NORMAL)
        text_area.delete("1.0", tk.END)
        text_area.config(state=tk.DISABLED)

        # Clear the README.txt file.
        with open("README.txt", "w") as file:
            file.write("")  

        messagebox.showinfo("History Cleared", "Quiz history has been cleared.")

    clear_button = tk.Button(button_frame, text="Clear", font=normal_font, width=15, bg="orange", fg="black", command=clear_text)
    clear_button.grid(row=0, column=0, padx=10)

    close_button = tk.Button(button_frame, text="Close", font=normal_font, width=15, bg="red", fg="white", command=history_win.destroy)
    close_button.grid(row=0, column=1, padx=10)

    # Frame for the scrollable history text.
    frame = tk.Frame(history_win, bg="#ccf2cc")
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    text_area = tk.Text(frame, wrap=tk.WORD, font=normal_font, bg="white", padx=10, pady=10)
    scrollbar = tk.Scrollbar(frame, command=text_area.yview)
    text_area.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    try:
        with open("README.txt", "r") as file:
            content = file.read()
    except FileNotFoundError:
        content = "No quiz history found."

    text_area.insert(tk.END, content)
    text_area.config(state=tk.DISABLED)

# Create main window and setup interface.
app = tk.Tk()
app.title("math quiz")
app.geometry("500x520")
app.config(bg="#ccf2cc")

menu_frame = tk.Frame(app, bg="#ccf2cc")
menu_frame.pack(pady=30)

try:
    menu_img = Image.open("math.png")
    menu_img = menu_img.resize((100, 100))
    menu_img_tk = ImageTk.PhotoImage(menu_img)
    img_label = tk.Label(menu_frame, image=menu_img_tk, bg="#ccf2cc")
    img_label.image = menu_img_tk
    img_label.pack(pady=5)
except IOError:
    pass

tk.Label(menu_frame, text="Welcome to the math quiz!", font=title_font, bg="#ccf2cc").pack(pady=10)
tk.Label(menu_frame, text="Enter your name:", font=big_font, bg="#ccf2cc").pack()
name_input = tk.Entry(menu_frame, font=normal_font, width=30)
name_input.pack(pady=5)
tk.Label(menu_frame, text="Choose difficulty:", font=big_font, bg="#ccf2cc").pack(pady=(20, 5))

difficulty = tk.StringVar(value="easy")
for level in ["easy", "medium", "hard"]:
    tk.Radiobutton(menu_frame, text=level, variable=difficulty, value=level, font=normal_font, bg="#ccf2cc").pack(anchor="w", padx=150)

button_frame = tk.Frame(menu_frame, bg="#ccf2cc")
button_frame.pack(pady=20)
tk.Button(button_frame, text="start quiz", font=normal_font, width=button_width, bg="green", fg="white", command=start_quiz).grid(row=0, column=0, padx=10)
tk.Button(button_frame, text="quit", font=normal_font, width=button_width, bg="red", fg="white", command=quit_game).grid(row=0, column=1, padx=10)

# view history button to view quiz history
tk.Button(menu_frame, text="view history", font=normal_font, width=button_width, bg="darkblue", fg="white", command=view_history).pack(pady=5)

quiz_frame = tk.Frame(app, bg="#ccf2cc")

# NEW difficulty title label
difficulty_title = tk.Label(quiz_frame, text="", font=title_font, bg="#ccf2cc")
difficulty_title.pack(pady=(10, 0))

question_text = tk.Label(quiz_frame, text="", font=big_font, wraplength=500, bg="#ccf2cc")
question_text.pack(pady=20)
image_box = tk.Label(quiz_frame, bg="#ccf2cc")
image_box.pack()
answer_input = tk.Entry(quiz_frame, font=normal_font, width=30)
answer_input.pack(pady=10)
tk.Button(quiz_frame, text="submit answer", font=normal_font, width=button_width, bg="blue", fg="white", command=submit_answer).pack(pady=5)
tk.Button(quiz_frame, text="previous question", font=normal_font, width=button_width, bg="purple", fg="white", command=go_back).pack(pady=5)
tk.Button(quiz_frame, text="Main Menu", font=normal_font, width=button_width, bg="orange", fg="black", command=back_to_menu).pack(pady=5)
tk.Button(quiz_frame, text="quit", font=normal_font, width=button_width, bg="red", fg="white", command=quit_game).pack(pady=5)

app.mainloop()
