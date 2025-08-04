import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random

# Easy questions generator
def make_easy_questions():
    quiz = []
    for _ in range(3):
        a = random.randint(1, 20)
        b = random.randint(1, 20)
        op = random.choice(["+", "-", "*", "/"])

        if op == "+":
            question = f"What is {a} + {b}?"
            answer = str(a + b)
        elif op == "-":
            question = f"What is {a} - {b}?"
            answer = str(a - b)
        elif op == "*":
            question = f"What is {a} × {b}?"
            answer = str(a * b)
        elif op == "/":
            a = a * b  # make it divisible
            question = f"What is {a} ÷ {b}?"
            answer = str(a // b)

        quiz.append({"question": question, "answer": answer})
    return quiz

# Medium difficulty with images
medium_questions = [
    {"image": "rectangle.png", "question": "What is the area of a 10 × 5 rectangle?", "answer": "50"},
    {"image": "triangle.png", "question": "What is the area of a triangle with base 10 and height 4?", "answer": "20"},
    {"image": "circle.png", "question": "What is the area of a circle with radius 3? (Use 3.14)", "answer": "28.26"}
]

# Placeholder for hard
hard_questions = [{"question": "IDK", "answer": ""}]

# Main setup
app = tk.Tk()
app.title("Math Quiz")
app.geometry("600x500")
app.config(bg="white")

# Quiz state
questions = []
current = 0
score = 0

# === Main Menu ===
menu = tk.Frame(app, bg="white")
menu.pack(pady=30)

tk.Label(menu, text="Welcome to the Math Quiz!", font=("Arial", 20), bg="white").pack(pady=10)

tk.Label(menu, text="Your name:", font=("Arial", 14), bg="white").pack()
name_input = tk.Entry(menu, font=("Arial", 14), width=30)
name_input.pack(pady=5)

tk.Label(menu, text="Choose difficulty:", font=("Arial", 14), bg="white").pack(pady=(20, 5))
difficulty = tk.StringVar(value="Easy")

for level in ["Easy", "Medium", "Hard"]:
    tk.Radiobutton(menu, text=level, variable=difficulty, value=level,
                   font=("Arial", 12), bg="white").pack(anchor="w", padx=150)

def start_quiz():
    global questions, current, score
    name = name_input.get().strip()
    if name == "":
        messagebox.showwarning("Oops!", "Please type your name.")
        return

    current = 0
    score = 0
    level = difficulty.get()

    if level == "Easy":
        questions = make_easy_questions()
    elif level == "Medium":
        questions = medium_questions
    else:
        questions = hard_questions

    menu.pack_forget()
    quiz_frame.pack()
    show_question()

def quit_game():
    if messagebox.askyesno("Exit", "Leave the quiz?"):
        app.destroy()

btn_frame = tk.Frame(menu, bg="white")
btn_frame.pack(pady=20)
tk.Button(btn_frame, text="Start", font=("Arial", 12), width=15,
          bg="green", fg="white", command=start_quiz).grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="Quit", font=("Arial", 12), width=15,
          bg="red", fg="white", command=quit_game).grid(row=0, column=1, padx=10)

# === Quiz Screen ===
quiz_frame = tk.Frame(app, bg="white")

question_text = tk.Label(quiz_frame, text="", font=("Arial", 16), wraplength=500, bg="white")
question_text.pack(pady=20)

image_box = tk.Label(quiz_frame, bg="white")
image_box.pack()

answer_input = tk.Entry(quiz_frame, font=("Arial", 14), width=30)
answer_input.pack(pady=10)

def show_question():
    q = questions[current]
    question_text.config(text=q["question"])

    if "image" in q:
        try:
            img = Image.open(q["image"]).resize((300, 200))
            photo = ImageTk.PhotoImage(img)
            image_box.config(image=photo, text="")
            image_box.image = photo
        except:
            image_box.config(text="(Image not found)", image="")
    else:
        image_box.config(image="", text="")
        image_box.image = None

    answer_input.delete(0, tk.END)
    answer_input.focus()

def check():
    global current, score
    user_answer = answer_input.get().strip()
    right = questions[current]["answer"]

    if user_answer == right:
        score += 1
        messagebox.showinfo("✅ Correct", "Good job!")
    else:
        if right == "":
            messagebox.showinfo("Hmm...", "No answer was set for this question.")
        else:
            messagebox.showinfo("❌ Incorrect", f"The right answer was: {right}")

    current += 1
    if current < len(questions):
        show_question()
    else:
        messagebox.showinfo("Done!", f"You got {score} out of {len(questions)} right.")
        app.destroy()

tk.Button(quiz_frame, text="Submit Answer", font=("Arial", 12), width=20,
          bg="blue", fg="white", command=check).pack(pady=10)

tk.Button(quiz_frame, text="Quit", font=("Arial", 12), width=20,
          bg="red", fg="white", command=quit_game).pack(pady=5)

# Start the app
app.mainloop()
