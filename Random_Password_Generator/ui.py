import tkinter as tk
from tkinter import font as tkfont, messagebox
import os
import sys

import generator
import security
import storage

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Password Generator")
        self.root.geometry("850x650")  # Widened for the history panel
        self.icon = tk.PhotoImage(
    file=resource_path("assets/password.png")
)
        self.root.iconphoto(False, self.icon)
        self.root.resizable(False, False)
        self.root.configure(bg="#1E1B2E")

        self.settings = storage.load_settings()
        self.history = []

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.setup_fonts_and_colors()
        self.setup_menu()
        self.setup_ui()
        self.apply_loaded_settings()

        try:
            icon_img = tk.PhotoImage(file=os.path.join("assets", "icon.png"))
            self.root.iconphoto(False, icon_img)
        except Exception:
            pass 

    def setup_fonts_and_colors(self):
        self.heading_font = tkfont.Font(family="Segoe UI", size=20, weight="bold")
        self.label_font = tkfont.Font(family="Segoe UI", size=10)
        self.chk_font = tkfont.Font(family="Segoe UI", size=10)
        self.entry_font = tkfont.Font(family="Courier New", size=13, weight="bold")
        self.hist_font = tkfont.Font(family="Courier New", size=11)

        self.BG = "#1E1B2E"
        self.CARD_BG = "#2A2640"
        self.PANEL_BG = "#221F36"
        self.ACCENT = "#7C6FCD"
        self.ENTRY_BG = "#13111F"
        self.TEXT = "#F0EEF8"
        self.MUTED = "#9491A7"

        self.BAR_SEGMENTS = 10
        self.BAR_W = 28
        self.BAR_H = 14
        self.BAR_GAP = 3
        self.BAR_EMPTY = "#2E2A42"

    def setup_menu(self):
        menubar = tk.Menu(self.root)
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        self.root.config(menu=menubar)

    def show_about(self):
        about_text = (
            "Advanced Password Generator\n"
            "Version 1.0\n\n"
            "Features:\n"
            "• Secure password generation\n"
            "• Password strength analysis\n"
            "• Entropy calculation\n"
            "• Clipboard integration\n"
            "• Security policy presets\n\n"
            "Built with Python and Tkinter."
        )
        messagebox.showinfo("About", about_text)

    def apply_loaded_settings(self):
        self.length_var.set(str(self.settings.get("length", 16)))
        self.var_upper.set(self.settings.get("uppercase", True))
        self.var_lower.set(self.settings.get("lowercase", True))
        self.var_digits.set(self.settings.get("numbers", True))
        self.var_symbols.set(self.settings.get("symbols", True))
        self.var_exclude_ambig.set(self.settings.get("exclude_ambiguous", False))
        self.var_prevent_rep.set(self.settings.get("prevent_repeats", True))

        policy = self.settings.get("policy", "Enterprise")
        self.policy_var.set(policy)
        self.lbl_policy_val.config(text=policy)


    def on_closing(self):
        self.settings = {
            "length": int(self.length_var.get()),
            "uppercase": self.var_upper.get(),
            "lowercase": self.var_lower.get(),
            "numbers": self.var_digits.get(),
            "symbols": self.var_symbols.get(),
            "exclude_ambiguous": self.var_exclude_ambig.get(),
            "prevent_repeats": self.var_prevent_rep.get(),
            "policy": self.policy_var.get()
        }
        storage.save_settings(self.settings)
        self.root.destroy()

    def setup_ui(self):
        left_frame = tk.Frame(self.root, bg=self.BG)
        left_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        right_frame = tk.Frame(self.root, bg=self.CARD_BG, width=300)
        right_frame.pack(side="right", fill="y", padx=(0, 20), pady=20)

        tk.Label(left_frame, text="Advanced Password Generator", font=self.heading_font, bg=self.BG, fg=self.TEXT).pack(
            anchor="w")
        tk.Frame(left_frame, bg=self.ACCENT, height=2, width=400).pack(anchor="w", pady=(5, 15))

        ctrl_frame = tk.Frame(left_frame, bg=self.BG)
        ctrl_frame.pack(fill="x", pady=5)

        tk.Label(ctrl_frame, text="Length:", font=self.label_font, bg=self.BG, fg=self.MUTED).pack(side="left")
        self.length_var = tk.StringVar()
        tk.Spinbox(ctrl_frame, from_=8, to=128, textvariable=self.length_var, width=4).pack(side="left", padx=10)

        tk.Label(ctrl_frame, text="Policy:", font=self.label_font, bg=self.BG, fg=self.MUTED).pack(side="left",
                                                                                                   padx=(15, 5))
        self.policy_var = tk.StringVar()
        policy_menu = tk.OptionMenu(ctrl_frame, self.policy_var, "Custom", "Standard", "Strong", "Enterprise",
                                    command=self.apply_policy)
        policy_menu.pack(side="left")

        chk_frame = tk.Frame(left_frame, bg=self.PANEL_BG)
        chk_frame.pack(fill="x", pady=10, ipadx=10, ipady=10)

        self.var_upper = tk.BooleanVar()
        self.var_lower = tk.BooleanVar()
        self.var_digits = tk.BooleanVar()
        self.var_symbols = tk.BooleanVar()
        self.var_exclude_ambig = tk.BooleanVar()
        self.var_prevent_rep = tk.BooleanVar()

        self.create_check(chk_frame, self.var_upper, "☑ Uppercase")
        self.create_check(chk_frame, self.var_lower, "☑ Lowercase")
        self.create_check(chk_frame, self.var_digits, "☑ Numbers")
        self.create_check(chk_frame, self.var_symbols, "☑ Symbols")
        tk.Frame(chk_frame, bg=self.BG, height=1).pack(fill="x", pady=5)
        self.create_check(chk_frame, self.var_exclude_ambig, "☑ Exclude Ambiguous (0, O, l, 1)")
        self.create_check(chk_frame, self.var_prevent_rep, "☑ Prevent Repeated Characters")

        self.password_var = tk.StringVar()
        tk.Entry(left_frame, textvariable=self.password_var, font=self.entry_font, justify="center", bg="white",
                 fg="black", readonlybackground="white", state="readonly").pack(fill="x", ipady=12, pady=10)

        btn_frame = tk.Frame(left_frame, bg=self.BG)
        btn_frame.pack(fill="x", pady=5)
        tk.Button(btn_frame, text="⚡ Generate Password", bg=self.ACCENT, fg=self.TEXT, font=("Segoe UI", 11, "bold"),
                  command=self.generate_password).pack(side="left", expand=True, fill="x", padx=(0, 5), ipady=5)
        tk.Button(btn_frame, text="📋 Copy", bg=self.PANEL_BG, fg=self.TEXT, font=("Segoe UI", 11, "bold"),
                  command=self.copy_password).pack(side="left", expand=True, fill="x", padx=(5, 0), ipady=5)

        info_frame = tk.Frame(left_frame, bg=self.PANEL_BG)
        info_frame.pack(fill="x", pady=15, ipadx=10, ipady=10)
        self.lbl_strength_val = self.add_info_row(info_frame, "Strength:")
        self.lbl_entropy_val = self.add_info_row(info_frame, "Entropy:")
        self.lbl_policy_val = self.add_info_row(info_frame, "Active Policy:")

        canvas_total_w = self.BAR_SEGMENTS * (self.BAR_W + self.BAR_GAP) - self.BAR_GAP
        self.canvas_bar = tk.Canvas(left_frame, width=canvas_total_w, height=self.BAR_H, bg=self.BG,
                                    highlightthickness=0)
        self.canvas_bar.pack(pady=(0, 15))

        for i in range(self.BAR_SEGMENTS):
            x0 = i * (self.BAR_W + self.BAR_GAP)
            self.canvas_bar.create_rectangle(x0, 0, x0 + self.BAR_W, self.BAR_H, fill=self.BAR_EMPTY, outline="")

        tk.Label(right_frame, text="Recent Passwords", font=("Segoe UI", 14, "bold"), bg=self.CARD_BG,
                 fg=self.TEXT).pack(pady=(15, 5))

        self.history_listbox = tk.Listbox(right_frame, font=self.hist_font, bg=self.ENTRY_BG, fg=self.TEXT, bd=0,
                                          highlightthickness=0, selectbackground=self.ACCENT)
        self.history_listbox.pack(fill="both", expand=True, padx=15, pady=10)

        tk.Button(right_frame, text="💾 Export History", bg=self.PANEL_BG, fg=self.TEXT,
                  command=lambda: storage.export_history_to_txt(self.history)).pack(fill="x", padx=15, pady=(0, 5),
                                                                                    ipady=3)
        tk.Button(right_frame, text="🗑 Clear History", bg="#E05C5C", fg="white", command=self.clear_history).pack(
            fill="x", padx=15, pady=(0, 15), ipady=3)

    def create_check(self, parent, var, text):
        tk.Checkbutton(parent, text=text, variable=var, bg=self.PANEL_BG, fg=self.TEXT, selectcolor=self.ENTRY_BG,
                       font=self.chk_font, activebackground=self.PANEL_BG, activeforeground=self.TEXT).pack(anchor="w",
                                                                                                            padx=10)

    def add_info_row(self, parent, text):
        row = tk.Frame(parent, bg=self.PANEL_BG)
        row.pack(fill="x", pady=2)
        tk.Label(row, text=text, font=self.label_font, bg=self.PANEL_BG, fg=self.MUTED).pack(side="left")
        val = tk.Label(row, text="--", font=("Segoe UI", 10, "bold"), bg=self.PANEL_BG, fg=self.TEXT)
        val.pack(side="right")
        return val

    def apply_policy(self, selection):
        if selection == "Standard":
            self.var_upper.set(True);
            self.var_lower.set(True);
            self.var_digits.set(True);
            self.var_symbols.set(False)
            self.var_exclude_ambig.set(False);
            self.var_prevent_rep.set(False)
            self.length_var.set("8")
        elif selection == "Strong":
            self.var_upper.set(True);
            self.var_lower.set(True);
            self.var_digits.set(True);
            self.var_symbols.set(True)
            self.var_exclude_ambig.set(False);
            self.var_prevent_rep.set(False)
            self.length_var.set("12")
        elif selection == "Enterprise":
            self.var_upper.set(True);
            self.var_lower.set(True);
            self.var_digits.set(True);
            self.var_symbols.set(True)
            self.var_exclude_ambig.set(False);
            self.var_prevent_rep.set(True)
            self.length_var.set("16")
        self.lbl_policy_val.config(text=selection)

    def generate_password(self):
        try:
            length = int(self.length_var.get())
            pwd, pool_size, _ = generator.generate_custom_password(
                length, self.var_upper.get(), self.var_lower.get(),
                self.var_digits.get(), self.var_symbols.get(),
                self.var_exclude_ambig.get(), self.var_prevent_rep.get()
            )
            self.password_var.set(pwd)
            self.update_security_panel(pwd, pool_size)
            self.add_to_history(pwd)

            if self.policy_var.get() not in ["Standard", "Strong", "Enterprise"]:
                self.lbl_policy_val.config(text="Custom")

        except ValueError as e:
            messagebox.showerror("Validation Error", str(e))

    def update_security_panel(self, pwd, pool_size):
        score, category = security.calculate_strength(pwd)
        entropy = security.calculate_entropy(len(pwd), pool_size)

        colour = security.STRENGTH_COLOURS.get(category, self.TEXT)

        self.lbl_strength_val.config(text=category, fg=colour)
        self.lbl_entropy_val.config(text=f"{entropy:.1f} bits")

        filled = round(self.BAR_SEGMENTS * score / 7)
        self.canvas_bar.delete("all")
        for i in range(self.BAR_SEGMENTS):
            x0 = i * (self.BAR_W + self.BAR_GAP)
            x1 = x0 + self.BAR_W
            fill = colour if i < filled else self.BAR_EMPTY
            self.canvas_bar.create_rectangle(x0, 0, x1, self.BAR_H, fill=fill, outline="")

    def copy_password(self):
        pwd = self.password_var.get()
        if not pwd:
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(pwd)
        self.root.update()

    def add_to_history(self, pwd):
        if self.history and self.history[0] == pwd:
            return

        self.history.insert(0, pwd)
        if len(self.history) > 10:
            self.history.pop()

        self.history_listbox.delete(0, tk.END)
        for p in self.history:
            self.history_listbox.insert(tk.END, p)

    def clear_history(self):
        if not self.history:
            return
        if messagebox.askyesno("Clear History", "Are you sure you want to clear the password history?"):
            self.history.clear()
            self.history_listbox.delete(0, tk.END)
