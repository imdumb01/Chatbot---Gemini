import google.generativeai as ai
import time
import tkinter as tk
from tkinter import scrolledtext
import threading

Api_key = ""
ai.configure(api_key=Api_key)
model = ai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat()


def insert_text(tag, text):
    text_area.config(state=tk.NORMAL)   
    text_area.insert(tk.END, text, tag)
    text_area.see(tk.END)
    text_area.config(state=tk.DISABLED)

def get_response(user_input):
    if user_input.lower() in ["bye", "quit", "see ya"]:
        insert_text("bot", "Chatbot: Bye.\n\n")
        return

    response = chat.send_message(user_input)
    clean_text = response.text.strip().replace("*", "").split()

    insert_text("bot", "Chatbot: ")
    # typing effect
    for word in clean_text:
        insert_text("bot", word + " ")
        time.sleep(0.1)
    insert_text("bot", "\n\n")

def send_message():
    user_input = entry.get().strip()
    if not user_input:
        return

    insert_text("user", "You: " + user_input + "\n")
    entry.delete(0, tk.END)

    threading.Thread(target=get_response, args=(user_input,), daemon=True).start()


root = tk.Tk()
root.title("AI Chatbot (Gemini)")
root.resizable(False , False)
root.geometry("700x1000")
root.configure(bg="#1e1e1e")


text_area = scrolledtext.ScrolledText(
    root, wrap=tk.WORD, font=("Segoe UI", 20),
    bg="#252526", fg="#e6e6e6", insertbackground="white",
    state=tk.DISABLED
)
text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)


text_area.tag_config("user", foreground="#4fc3f7")
text_area.tag_config("bot", foreground="#a5d6a7")


frame = tk.Frame(root, bg="#1e1e1e")
frame.pack(fill=tk.X, padx=10, pady=10)

entry = tk.Entry(
    frame, font=("Segoe UI", 12),
    bg="#2d2d2d", fg="white", insertbackground="white",
    relief="flat", bd=8
)
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), ipady=8)

send_button = tk.Button(
    frame, text="Send", command=send_message,
    font=("Segoe UI", 12, "bold"),
    bg="#0d6efd", fg="white", activebackground="#0b5ed7",
    relief="flat", padx=20, pady=8
)
send_button.pack(side=tk.RIGHT)


root.bind("<Return>", lambda event: send_message())


root.mainloop()

