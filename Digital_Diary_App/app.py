import tkinter as tk
from tkinter import ttk, messagebox
import os
from datetime import datetime

# ---------- MACOS STYLE CONFIG ----------
BG = "#ECECEC"               # MacOS grey background
CARD = "#FFFFFF"             # White card panel
ACCENT = "#007AFF"           # MacOS Blue
FONT = ("Segoe UI", 11)
TITLE_FONT = ("Segoe UI", 16, "bold")

PASSWORD_FILE = "password.txt"
DIARY_FILE = "diary.txt"
DEFAULT_PASSWORD = "admin123"

# ---------- PASSWORD HELPERS ----------
def load_password():
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, "r") as f:
            return f.read().strip()
    return DEFAULT_PASSWORD

def save_password(new):
    with open(PASSWORD_FILE, "w") as f:
        f.write(new)

# ---------- LOGIN WINDOW ----------
class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Diary Login")
        self.root.geometry("420x300")
        self.root.config(bg=BG)
        self.root.resizable(False, False)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Card.TFrame", background=CARD)
        style.configure("TLabel", background=CARD, font=FONT)
        style.configure("Big.TLabel", background=CARD, font=TITLE_FONT)
        style.configure("Accent.TButton",
                        background=ACCENT,
                        foreground="white",
                        font=("Segoe UI", 11, "bold"),
                        padding=6)
        style.map("Accent.TButton",
                  background=[("active", "#005FCC")])

        card = ttk.Frame(self.root, padding=25, style="Card.TFrame")
        card.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(card, text="Welcome Back", style="Big.TLabel").pack(pady=(0, 10))
        ttk.Label(card, text="Enter your password to continue").pack(pady=(0, 12))

        ttk.Label(card, text="Password").pack(anchor="w")
        self.pwd = ttk.Entry(card, show="*", width=30)
        self.pwd.pack(pady=(2, 15))

        ttk.Button(card, text="Login", style="Accent.TButton",
                   command=self.check_password).pack()

        ttk.Label(card, text="Default password: admin123",
                  font=("Segoe UI", 9), foreground="#888888",
                  background=CARD).pack(pady=10)

    def check_password(self):
        entered = self.pwd.get().strip()
        if entered == load_password():
            self.root.destroy()
            open_diary_window()
        else:
            messagebox.showerror("Error", "Incorrect password!")

# ---------- CHANGE PASSWORD WINDOW ----------
class ChangePasswordWindow:
    def __init__(self, master):
        self.top = tk.Toplevel(master)
        self.top.title("Change Password")
        self.top.geometry("400x250")
        self.top.config(bg=BG)
        self.top.resizable(False, False)

        style = ttk.Style()
        style.configure("Card.TFrame", background=CARD)
        style.configure("TLabel", background=CARD, font=FONT)
        style.configure("Accent.TButton",
                        background=ACCENT,
                        foreground="white",
                        font=("Segoe UI", 11, "bold"),
                        padding=6)

        card = ttk.Frame(self.top, padding=20, style="Card.TFrame")
        card.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(card, text="Change Password", font=TITLE_FONT, background=CARD).pack(pady=8)

        ttk.Label(card, text="Old Password").pack(anchor="w")
        self.old = ttk.Entry(card, show="*")
        self.old.pack(fill="x", pady=4)

        ttk.Label(card, text="New Password").pack(anchor="w")
        self.new = ttk.Entry(card, show="*")
        self.new.pack(fill="x", pady=4)

        ttk.Label(card, text="Confirm Password").pack(anchor="w")
        self.confirm = ttk.Entry(card, show="*")
        self.confirm.pack(fill="x", pady=4)

        ttk.Button(card, text="Update", style="Accent.TButton",
                   command=self.update_password).pack(pady=12)

    def update_password(self):
        if self.old.get() != load_password():
            messagebox.showerror("Error", "Old password incorrect!")
            return
        if self.new.get() != self.confirm.get():
            messagebox.showerror("Error", "New passwords do not match!")
            return
        if len(self.new.get()) < 4:
            messagebox.showwarning("Weak", "Password must be at least 4 characters.")
            return

        save_password(self.new.get())
        messagebox.showinfo("Success", "Password Updated!")
        self.top.destroy()

# ---------- MAIN DIARY WINDOW ----------
class DiaryWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Diary")
        self.root.geometry("920x620")
        self.root.config(bg=BG)

        style = ttk.Style()
        style.configure("Top.TFrame", background=BG)
        style.configure("Card.TFrame", background=CARD)
        style.configure("Title.TLabel", background=BG, font=TITLE_FONT)

        top = ttk.Frame(self.root, padding=15, style="Top.TFrame")
        top.pack(fill="x")

        ttk.Label(top, text="My Secure Digital Diary", style="Title.TLabel").pack(side="left")

        self.time_label = ttk.Label(top, background=BG, font=("Segoe UI", 10))
        self.time_label.pack(side="right")
        self.update_time()

        card = ttk.Frame(self.root, padding=10, style="Card.TFrame")
        card.pack(expand=True, fill="both", padx=20, pady=10)

        self.text = tk.Text(
            card,
            wrap="word",
            font=("Segoe UI", 12),
            bg="white",
            fg="#222222",
            relief="flat",
            padx=12,
            pady=10
        )
        self.text.pack(expand=True, fill="both")

        # Bind key release for word count
        self.text.bind("<KeyRelease>", self.update_word_count)

        # Buttons row
        btns = ttk.Frame(card, style="Card.TFrame")
        btns.pack(fill="x", pady=(10, 0))

        ttk.Button(btns, text="Load", command=self.load).pack(side="left", padx=4)
        ttk.Button(btns, text="Save", style="Accent.TButton", command=self.save).pack(side="left", padx=4)
        ttk.Button(btns, text="Clear", command=self.clear).pack(side="left", padx=4)
        ttk.Button(btns, text="Insert Time", command=self.insert_time).pack(side="left", padx=4)
        ttk.Button(btns, text="Change Password",
                   command=lambda: ChangePasswordWindow(self.root)).pack(side="right")

        # Status bar: word count + autosave label
        status = ttk.Frame(card, style="Card.TFrame")
        status.pack(fill="x", pady=(5, 0))

        self.word_label = ttk.Label(status, text="Words: 0", background=CARD, font=("Segoe UI", 9))
        self.word_label.pack(side="left")

        self.autosave_label = ttk.Label(status, text="", background=CARD, font=("Segoe UI", 9), foreground="#666666")
        self.autosave_label.pack(side="right")

        # Auto-save every 60 seconds
        self.autosave_interval_ms = 60000  # 60 seconds
        self.root.after(self.autosave_interval_ms, self.autosave)

        # Load initial text if available
        self.load(first=True)
        self.update_word_count()  # in case file already has content

    def update_time(self):
        now = datetime.now().strftime("%d %b %Y - %H:%M:%S")
        self.time_label.config(text=now)
        self.root.after(1000, self.update_time)

    def update_word_count(self, event=None):
        content = self.text.get("1.0", "end-1c")
        words = [w for w in content.split() if w.strip()]
        self.word_label.config(text=f"Words: {len(words)}")

    def autosave(self):
        content = self.text.get("1.0", "end-1c")
        try:
            with open(DIARY_FILE, "w", encoding="utf-8") as f:
                f.write(content)
            self.autosave_label.config(text="Autosaved just now")
        except Exception as e:
            self.autosave_label.config(text=f"Autosave failed: {e}")
        # schedule next autosave
        self.root.after(self.autosave_interval_ms, self.autosave)

    def load(self, first=False):
        if os.path.exists(DIARY_FILE):
            with open(DIARY_FILE, "r", encoding="utf-8") as f:
                self.text.delete("1.0", tk.END)
                self.text.insert(tk.END, f.read())
            if not first:
                messagebox.showinfo("Loaded", "Diary loaded successfully!")

    def save(self):
        with open(DIARY_FILE, "w", encoding="utf-8") as f:
            f.write(self.text.get("1.0", tk.END))
        self.autosave_label.config(text="Saved manually")

    def clear(self):
        if messagebox.askyesno("Confirm", "Clear everything?"):
            self.text.delete("1.0", tk.END)
            self.update_word_count()

    def insert_time(self):
        self.text.insert(tk.INSERT, f"\n[{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]\n")
        self.update_word_count()

# RUN APP
def open_diary_window():
    root = tk.Tk()
    DiaryWindow(root)
    root.mainloop()

def main():
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
