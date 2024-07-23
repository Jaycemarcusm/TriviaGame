import tkinter as tk
from tkinter import messagebox, ttk
from ttkbootstrap import Style
from quiz_data import quiz_data


def show_question():
   
    question = quiz_data[current_question]
    qs_label.config(text=question["question"])

    choices = question["choices"]
    for i in range(4):
        choice_btns[i].config(text=choices[i], state="normal") 

    feedback_label.config(text="")
    next_btn.config(state="disabled")


def add_question():
    def save_question():
       
        correct_index_str = correct_answer.get() 
        correct_index = int(correct_index_str) 

        correct_answer_text = entries[correct_index].get() 

        new_question = {
            "question": question_entry.get(),
            "choices": [entries[i].get() for i in range(4)],
            "answer": correct_answer_text 
        }

        save_to_quiz_data(new_question)

        add_question_window.destroy()

    add_question_window = tk.Toplevel(root)
    add_question_window.title("Add New Question")
    add_question_window.geometry("1024x576")

    tk.Label(add_question_window, text="Question:", font="Verdana").pack(pady=5)
    question_entry = tk.Entry(add_question_window)
    question_entry.pack(fill="x", padx=250, pady=10)

    entries = []
    for i in range(4):
        tk.Label(add_question_window, text=f"Choice {i + 1}:", font="Verdana").pack(pady=5)
        entry = tk.Entry(add_question_window)
        entry.pack(fill="x", padx=300, pady=5)
        entries.append(entry)

    tk.Label(add_question_window, text="Correct Answer:", font="Verdana").pack(pady=15)
    correct_answer = tk.StringVar() 
    for i in range(4):
        rb = tk.Radiobutton(add_question_window, variable=correct_answer,
                            value=str(i)) 
        rb.pack()

    tk.Button(add_question_window, text="Save Question", font="Verdana", command=save_question).pack(pady=20)


def save_to_quiz_data(new_question):
   
    with open("quiz_data.py", "r") as file:
        lines = file.readlines()

    end_of_quiz_data_line = None
    for i, line in enumerate(lines):
        if line.strip().endswith(']'):
            end_of_quiz_data_line = i
            break

    if end_of_quiz_data_line is not None:
       
        new_question_str = '    {\n' 
        new_question_str += '        "question": "' + new_question["question"].replace('"', '\\"') + '",\n'
        new_question_str += '        "choices": [' + ', '.join(['"' + choice.replace('"', '\\"') + '"'
                                                                for choice in new_question["choices"]]) + '],\n'
        new_question_str += '        "answer": "' + new_question["answer"].replace('"', '\\"') + '"\n' 
        new_question_str += '    },\n' 

        lines.insert(end_of_quiz_data_line, new_question_str)

        with open("quiz_data.py", "w") as file:
            file.writelines(lines)
    else:
        print("Error: Could not find the end of the quiz_data list.")


def check_answer(choice):
   
    question = quiz_data[current_question]
    selected_choice = choice_btns[choice].cget("text")

    if selected_choice == question["answer"]:
       
        global score
        score += 1
        score_label.config(text="Score: {}/{}".format(score, len(quiz_data)))
        feedback_label.config(text="That's right! Nice Job!", foreground="green")
    else:
        feedback_label.config(text="Yikes. Not even close.", foreground="red")

    for button in choice_btns:
        button.config(state="disabled")
    next_btn.config(state="normal")


def next_question():
    global current_question
    current_question += 1

    if current_question < len(quiz_data):
       
        show_question()
    else:
       
        messagebox.showinfo("Quiz Completed",
                            "You did it! You're free! \n Final score: {}/{}".format(score, len(quiz_data)))
        root.destroy()


root = tk.Tk()
root.title("Quiz App")
root.geometry("1280x720")
style = Style(theme="darkly")
style.configure("TLabel", font=("Verdana", 20))
style.configure("TButton", font=("Verdana", 16))

add_question_btn = ttk.Button(
    root,
    text="Add Question",
    command=add_question
)
add_question_btn.pack(pady=5)


def switch_theme(event=None):
    selected_theme = theme_combobox.get()
    style.theme_use(selected_theme)
    style.configure("TLabel", font=("Verdana", 20))
    style.configure("TButton", font=("Verdana", 16))


theme_combobox = ttk.Combobox(root, values=['darkly', 'flatly'], state='readonly')
theme_combobox.current(0)
theme_combobox.bind("<<ComboboxSelected>>", switch_theme)
theme_combobox.pack(anchor='nw')


qs_label = ttk.Label(
    root,
    anchor="center",
    wraplength=500,
    padding=10
)
qs_label.pack(pady=10)

choice_btns = []
for i in range(4):
    button = ttk.Button(
        root,
        command=lambda i=i: check_answer(i)
    )
    button.pack(pady=5)
    choice_btns.append(button)

feedback_label = ttk.Label(
    root,
    anchor="center",
    padding=10
)
feedback_label.pack(pady=10)

score = 0

score_label = ttk.Label(
    root,
    text="Score: 0/{}".format(len(quiz_data)),
    anchor="center",
    padding=10
)
score_label.pack(pady=10)

next_btn = ttk.Button(
    root,
    text="Next",
    command=next_question,
    state="disabled"
)
next_btn.pack(pady=10)

current_question = 0

show_question()

root.mainloop()
