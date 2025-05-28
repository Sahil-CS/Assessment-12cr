import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# List of 3 quiz questions with text only
quiz = [
    {"image": "rectangle.png", "question": "What is the area of a 10 × 5 rectangle?", "answer": "50"},
    {"image": "triangle.png", "question": "What is the area of a triangle with base 10 and height 4?", "answer": "20"},
    {"image": "circle.png", "question": "What is the area of a circle with radius 3? (Use 3.14)", "answer": "28.26"}
]

question_no = 0  # Which question are we on
students_score = 0  # 

# Check the answer
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

# Show current question and image
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

# GUI setup
root = tk.Tk()
root.title("Simple 3-Question Math Quiz")
root.geometry("600x500")

question_label = tk.Label(root, text="", font=("Arial", 14))
question_label.pack(pady=10)

image_label = tk.Label(root)
image_label.pack(pady=10)

answer_entry = tk.Entry(root, font=("Arial", 14))
answer_entry.pack(pady=10)

submit_button = tk.Button(root, text="Submit Answer", command=check_answer)
submit_button.pack(pady=10)

# Start with first question
show_question()

root.mainloop()
