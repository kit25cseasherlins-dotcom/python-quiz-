import tkinter as tk
import json
import os
import time

questions = [
   {"q": "Which keyword is used to import a module?", "options": ["a) include", "b) import", "c) using", "d) require"], "ans": 1}, 
   {"q": "Which module is used for math functions?", "options": ["a) random", "b) math", "c) sys", "d) os"], "ans": 1},
   {"q": "How do you access the first character of a string 'Python'?", "options": ["a) s[1]", "b) s[0]", "c) s[-1]", "d) s[2]"], "ans": 1},
   {"q": "What is the output of len('Hello')?", "options": ["a) 4", "b) 5", "c) 6", "d) Error"], "ans": 1},
   {"q": "Which method converts a string to uppercase?", "options": ["a) upper()", "b) uppercase()", "c) toUpper()", "d) cap()"], "ans": 0}, 
   {"q": "What does s[1:4] return?", "options": ["a) Characters from index 1 to 3", "b) 1 to 4", "c) Only index 4", "d) Error"], "ans": 0}, 
   {"q": "Strings in Python are:", "options": ["a) Mutable", "b) Immutable", "c) Dynamic", "d) Numeric"], "ans": 1}, 
   {"q": "Which function is used to find string length?", "options": ["a) size()", "b) count()", "c) len()", "d) length()"], "ans": 2}, 
   {"q": "Which operator is used for string concatenation?", "options": ["a) +", "b) *", "c) &", "d) %"], "ans": 0},
   {"q": "What is the output of 'Hi'*3?", "options": ["a) HiHiHi", "b) Hi3", "c) Error", "d) 3Hi"], "ans": 0}
]

class QuizApp:
    def start_quiz(self):
        self.player_name = "Player"

        # remove input UI
        self.name_label.destroy()
        self.name_entry.destroy()
        self.start_btn.destroy()

        self.start_time = time.time()

        # ✅ CREATE quiz UI here (after clicking start)
        self.q_label = tk.Label(self.root, text="", font=("Arial", 14), wraplength=400)
        self.q_label.pack(pady=20)

        self.timer_label = tk.Label(self.root, text="", font=("Arial", 12), fg="red")
        self.timer_label.place(x=400, y=10)

        self.buttons = []
        for i in range(4):
            btn = tk.Button(self.root, text="", width=20,
                            command=lambda i=i: self.check_answer(i))
            btn.pack(pady=5)
            self.buttons.append(btn)

        self.load_question()

    def __init__(self, root):

        self.root = root
        self.root.title("Quiz App")
        self.root.geometry("500x300")

        self.q_index = 0
        self.score = 0
        self.time_left = 20
        self.timer_id = None

        self.name_var = tk.StringVar()

        self.name_label = tk.Label(root, text="Enter your name:", font=("Arial", 12))
        self.name_label.pack()

        self.name_entry = tk.Entry(root, textvariable=self.name_var)
        self.name_entry.pack()

        self.start_btn = tk.Button(root, text="Start Quiz", command=self.start_quiz)
        self.start_btn.pack(pady=10)

    def load_question(self):
        # stop previous timer
        if self.timer_id:
            self.root.after_cancel(self.timer_id)

        if self.q_index >= len(questions):
            self.show_result()
            return

        q = questions[self.q_index]
        self.q_label.config(text=q["q"])

        for i, opt in enumerate(q["options"]):
            self.buttons[i].config(text=opt)

        self.time_left = 10
        self.update_timer()

    def update_timer(self):
        self.timer_label.config(text=f"⏳ {self.time_left}s")

        if self.time_left > 0:
            self.time_left -= 1
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.q_index += 1
            self.load_question()

    def check_answer(self, i):
        # stop timer when user clicks
        if self.timer_id:
            self.root.after_cancel(self.timer_id)

        q = questions[self.q_index]

        if i == q["ans"]:
            self.score += 1

        self.q_index += 1
        self.load_question()
    def show_result(self):
        import json, os, time

        total_time = int(time.time() - self.start_time)
        file = "leaderboard.json"

        # load existing data
        if os.path.exists(file):
            with open(file, "r") as f:
                leaderboard = json.load(f)
        else:
            leaderboard = []

        # add current player
        leaderboard.append({
            "name": self.player_name,
            "score": self.score,
            "time": total_time
        })

        # sort: score desc, time asc
        leaderboard.sort(key=lambda x: (-x["score"], x["time"]))

        # save
        with open(file, "w") as f:
            json.dump(leaderboard, f, indent=4)

        # 🧹 CLEAR SCREEN
        for widget in self.root.winfo_children():
            widget.destroy()

        # 🏆 Title
        title = tk.Label(self.root, text="🏆 LEADERBOARD", font=("Arial", 16))
        title.pack(pady=10)

        # 📊 Show top 5
        for i, p in enumerate(leaderboard[:5]):
            medal = ["🥇", "🥈", "🥉"]
            icon = medal[i] if i < 3 else ""

            minutes = p['time'] // 60
            seconds = p['time'] % 60
            time_str = f"{minutes:02}:{seconds:02}"

            lbl = tk.Label(
                self.root,
                text=f"{icon} {i+1}. {p['name']} - {p['score']} pts - {time_str}",
                font=("Arial", 12)
            )
            lbl.pack()
root = tk.Tk()
app = QuizApp(root)
root.mainloop()