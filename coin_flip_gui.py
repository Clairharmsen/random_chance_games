import random
import tkinter as tk
from tkinter import simpledialog, messagebox
import threading
import time

# Big input dialog
class BigIntegerDialog(simpledialog._QueryInteger):
    def body(self, master):
        tk.Label(master, text=self.prompt, font=("Helvetica", 24, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.entry = tk.Entry(master, font=("Helvetica", 22), width=10, justify='center')
        self.entry.grid(row=1, column=0, padx=10, pady=10)
        return self.entry

def big_ask_integer(title, prompt, **kwargs):
    return BigIntegerDialog(root, title, prompt, **kwargs).result

def flip():
    return "heads" if random.randint(1, 1000) > 500 else "tails"

def add_to_history(text):
    history_box.config(state="normal")
    history_box.insert("1.0", text + "\n")
    history_box.config(state="disabled")

def animate_flip_one():
    frames = [
        "   _______\n  /       \\\n |  HEADS  |\n  \\_______/",
        "   _______\n  /       \\\n | TAILS ? |\n  \\_______/",
        "   _______\n  /       \\\n | SPINNING|\n  \\_______/",
        "   _______\n  /       \\\n |  ? ? ?  |\n  \\_______/"
    ]

    for i in range(6):
        result_label.config(text=frames[i % len(frames)], fg="gray", font=("Courier", 20))
        time.sleep(0.2)

    result = flip().capitalize()
    art = f"""
   _______
  /       \\
 |  {result.upper():^7} |
  \\_______/
"""
    result_label.config(text=art, fg="navy", font=("Courier", 20))
    summary_label.config(text="")
    add_to_history(f"Flipped 1 coin → {result}")

def flip_one():
    threading.Thread(target=animate_flip_one).start()

def flip_multiple():
    try:
        count = big_ask_integer("🪙 How many?", "How many coins do you want to flip?")
        if count is None:
            return

        headcount = 0
        tailcount = 0

        for _ in range(count):
            if flip() == "heads":
                headcount += 1
            else:
                tailcount += 1

        head_percent = (headcount / count) * 100
        tail_percent = (tailcount / count) * 100

        result_label.config(text=f"🎯 Flipped {count:,} coins!", fg="darkgreen", font=("Helvetica", 32))
        summary_label.config(
            text=f"Heads 🧠: {headcount:,} ({head_percent:.2f}%)\n"
                 f"Tails 🌀: {tailcount:,} ({tail_percent:.2f}%)",
            fg="black"
        )
        add_to_history(
            f"Flipped {count:,} → Heads: {headcount:,} ({head_percent:.2f}%), "
            f"Tails: {tailcount:,} ({tail_percent:.2f}%)"
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))

def toggle_history():
    if history_box.winfo_ismapped():
        history_box.pack_forget()
        toggle_button.config(text="Show History")
    else:
        history_box.pack(pady=15)
        toggle_button.config(text="Hide History")

# Main window
root = tk.Tk()
root.title("🪙 Coin Flipper with Realistic Animation")
root.geometry("900x700")
root.configure(bg="#f0f4ff")

# Main content frame (centered)
main_frame = tk.Frame(root, bg="#f0f4ff")
main_frame.pack(expand=True)

# Title
title = tk.Label(main_frame, text="🪙 Coin Flipper Deluxe", font=("Helvetica", 36, "bold"), bg="#f0f4ff")
title.pack(pady=20)

# Result & Summary
result_label = tk.Label(main_frame, text="", font=("Courier", 20), bg="#f0f4ff", justify="center")
result_label.pack(pady=10)

summary_label = tk.Label(main_frame, text="", font=("Helvetica", 28), bg="#f0f4ff", justify="center")
summary_label.pack(pady=10)

# Buttons
btn_one = tk.Button(main_frame, text="Flip ONE Coin", font=("Helvetica", 28), width=20, bg="#d1e7ff", command=flip_one)
btn_one.pack(pady=10)

btn_multi = tk.Button(main_frame, text="Flip MULTIPLE Coins", font=("Helvetica", 28), width=20, bg="#bfefff", command=flip_multiple)
btn_multi.pack(pady=10)

toggle_button = tk.Button(main_frame, text="Show History", font=("Helvetica", 20), width=20, bg="#eee0ff", command=toggle_history)
toggle_button.pack(pady=5)

btn_quit = tk.Button(main_frame, text="QUIT", font=("Helvetica", 28), width=20, bg="#ffc1c1", command=root.quit)
btn_quit.pack(pady=10)

# History (centered under buttons, toggled)
history_box = tk.Text(main_frame, font=("Helvetica", 16), height=10, width=70, state="disabled", bg="#ffffff", wrap="word")
# (not packed until toggled)

# Run the GUI
root.mainloop()