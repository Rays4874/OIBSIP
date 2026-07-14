import tkinter as tk
from tkinter import font as tkfont, messagebox
import secrets
import string
import math

root = tk.Tk()
root.title("Advanced Password Generator")
root.geometry("550x850")
root.resizable(False, False)
root.configure(bg="#1E1B2E")

heading_font = tkfont.Font(family="Segoe UI", size=20, weight="bold")
subtext_font = tkfont.Font(family="Segoe UI", size=10)
label_font = tkfont.Font(family="Segoe UI", size=10)
section_font = tkfont.Font(family="Segoe UI", size=10, weight="bold")
chk_font = tkfont.Font(family="Segoe UI", size=10)
button_font = tkfont.Font(family="Segoe UI", size=11, weight="bold")
entry_font = tkfont.Font(family="Courier New", size=13, weight="bold")
spinbox_font = tkfont.Font(family="Segoe UI", size=11, weight="bold")
strength_font = tkfont.Font(family="Segoe UI", size=10, weight="bold")

BG = "#1E1B2E"
CARD_BG = "#2A2640"
PANEL_BG = "#221F36"
ACCENT = "#7C6FCD"
ACCENT_HV = "#9B8EE0"
ENTRY_BG = "#FFFFFF"
ENTRY_FG = "#000000"
SPIN_BG = "#13111F"
SPIN_FG = "#F0EEF8"
TEXT = "#F0EEF8"
MUTED = "#9491A7"
CHK_SEL = "#A8F0C6"
BAR_EMPTY = "#2E2A42"

STRENGTH_COLOURS = {
    "Not Generated": MUTED,
    "Weak": "#E05C5C",
    "Medium": "#E09A3A",
    "Strong": "#4CAF75",
    "Very Strong": "#00E676",
}


def calculate_strength(password: str) -> tuple[int, str]:
    score = 0
    n = len(password)

    if n >= 16:
        score += 3
    elif n >= 12:
        score += 2
    elif n >= 8:
        score += 1

    if any(c in string.ascii_uppercase for c in password): score += 1
    if any(c in string.ascii_lowercase for c in password): score += 1
    if any(c in string.digits for c in password): score += 1
    if any(c not in string.ascii_letters + string.digits for c in password): score += 1

    if score <= 2:
        category = "Weak"
    elif score <= 4:
        category = "Medium"
    elif score <= 6:
        category = "Strong"
    else:
        category = "Very Strong"

    return score, category


BAR_SEGMENTS = 10
BAR_W, BAR_H = 28, 14
BAR_GAP = 3


def update_security_panel(password: str, pool_size: int, types_count: int) -> None:
    score, category = calculate_strength(password)
    colour = STRENGTH_COLOURS[category]
    lbl_strength_val.config(text=category, fg=colour)

    if pool_size > 0:
        entropy = len(password) * math.log2(pool_size)
        lbl_entropy_val.config(text=f"{entropy:.1f} bits")
    else:
        lbl_entropy_val.config(text="0.0 bits")

    lbl_types_val.config(text=str(types_count))

    filled = round(BAR_SEGMENTS * score / 7)
    canvas_bar.delete("all")
    for i in range(BAR_SEGMENTS):
        x0 = i * (BAR_W + BAR_GAP)
        x1 = x0 + BAR_W
        fill = colour if i < filled else BAR_EMPTY
        canvas_bar.create_rectangle(x0, 0, x1, BAR_H, fill=fill, outline="")


def apply_policy(selection):
    if selection == "Standard":
        var_upper.set(True);
        var_lower.set(True);
        var_digits.set(True);
        var_symbols.set(False)
        var_exclude_ambig.set(False);
        var_prevent_rep.set(False)
        length_var.set("8")
    elif selection == "Strong":
        var_upper.set(True);
        var_lower.set(True);
        var_digits.set(True);
        var_symbols.set(True)
        var_exclude_ambig.set(False);
        var_prevent_rep.set(False)
        length_var.set("12")
    elif selection == "Enterprise":
        var_upper.set(True);
        var_lower.set(True);
        var_digits.set(True);
        var_symbols.set(True)
        var_exclude_ambig.set(False);
        var_prevent_rep.set(True)
        length_var.set("16")

    lbl_policy_val.config(text=selection)


def generate_password():
    try:
        length = int(length_var.get())
    except ValueError:
        length = 12
    length = max(8, min(128, length))
    length_var.set(str(length))

    pool_str = ""
    mandatory_groups = []

    if var_upper.get():
        pool_str += string.ascii_uppercase
        mandatory_groups.append(string.ascii_uppercase)
    if var_lower.get():
        pool_str += string.ascii_lowercase
        mandatory_groups.append(string.ascii_lowercase)
    if var_digits.get():
        pool_str += string.digits
        mandatory_groups.append(string.digits)
    if var_symbols.get():
        symbols = "!@#$%^&*()-_=+[]{}|;:,.<>?/"
        pool_str += symbols
        mandatory_groups.append(symbols)

    if not pool_str:
        messagebox.showerror("Error", "Please select at least one character type.")
        return

    if var_exclude_ambig.get():
        ambiguous = "0OIl15S2Z"
        pool_str = "".join([c for c in pool_str if c not in ambiguous])
        cleaned_groups = []
        for group in mandatory_groups:
            clean_group = "".join([c for c in group if c not in ambiguous])
            if clean_group:
                cleaned_groups.append(clean_group)
        mandatory_groups = cleaned_groups

    if not pool_str:
        messagebox.showerror("Error", "Excluding ambiguous characters left the pool empty.")
        return

    pool_size = len(set(pool_str))

    if var_prevent_rep.get():
        if length > pool_size:
            messagebox.showerror(
                "Pool Exhausted",
                f"Cannot generate a {length}-character password without repeating characters. "
                f"Only {pool_size} unique characters are available in your selected pools."
            )
            return

        available = set(pool_str)
        chars = []

        for group in mandatory_groups:
            valid_choices = list(set(group) & available)
            if valid_choices:
                choice = secrets.choice(valid_choices)
                chars.append(choice)
                available.remove(choice)

        if len(chars) < length:
            secure_sampler = secrets.SystemRandom()
            chars.extend(secure_sampler.sample(list(available), length - len(chars)))

    else:
        guaranteed = [secrets.choice(g) for g in mandatory_groups]
        filler = [secrets.choice(pool_str) for _ in range(length - len(guaranteed))]
        chars = guaranteed + filler

    for i in range(len(chars) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        chars[i], chars[j] = chars[j], chars[i]

    password = "".join(chars)
    password_var.set(password)

    if policy_var.get() not in ["Standard", "Strong", "Enterprise"]:
        lbl_policy_val.config(text="Custom")

    update_security_panel(password, pool_size, len(mandatory_groups))
    copy_status_var.set("") 


def copy_password():
    password = password_var.get()
    if not password:
        messagebox.showwarning("Copy Failed", "Please generate a password first.")
        return

    root.clipboard_clear()
    root.clipboard_append(password)
    root.update()

    copy_status_var.set("✓ Copied")
    root.after(2500, lambda: copy_status_var.set(""))


tk.Frame(root, bg=ACCENT, height=4).pack(fill="x", side="top")

card = tk.Frame(root, bg=CARD_BG, bd=0, relief="flat")
card.place(relx=0.5, rely=0.5, anchor="center", width=480, height=760)

tk.Label(card, text="🔐", font=("Segoe UI Emoji", 28), bg=CARD_BG, fg=ACCENT).pack(pady=(16, 2))
tk.Label(card, text="Advanced Password Generator", font=heading_font, bg=CARD_BG, fg=TEXT).pack(pady=(0, 2))
tk.Label(card, text="Secure · Customisable · Instant", font=subtext_font, bg=CARD_BG, fg=MUTED).pack(pady=(0, 8))
tk.Frame(card, bg=ACCENT, height=1, width=380).pack(pady=(0, 10))

controls_row = tk.Frame(card, bg=CARD_BG)
controls_row.pack(pady=(0, 10), fill="x", padx=32)

tk.Label(controls_row, text="Length:", font=label_font, bg=CARD_BG, fg=MUTED).pack(side="left")
length_var = tk.StringVar(value="16")
tk.Spinbox(
    controls_row, from_=8, to=128, textvariable=length_var,
    font=spinbox_font, width=4, justify="center",
    bd=0, bg=SPIN_BG, fg=SPIN_FG, buttonbackground=CARD_BG, wrap=False,
).pack(side="left", ipady=3, padx=(6, 20))

tk.Label(controls_row, text="Policy:", font=label_font, bg=CARD_BG, fg=MUTED).pack(side="left")
policy_var = tk.StringVar(value="Enterprise")
policy_menu = tk.OptionMenu(controls_row, policy_var, "Custom", "Standard", "Strong", "Enterprise",
                            command=apply_policy)
policy_menu.config(bg=PANEL_BG, fg=TEXT, activebackground=ENTRY_BG, activeforeground=TEXT, bd=0, highlightthickness=1,
                   highlightbackground=MUTED, font=label_font)
policy_menu["menu"].config(bg=PANEL_BG, fg=TEXT)
policy_menu.pack(side="left", padx=(6, 0), fill="x", expand=True)

chk_panel = tk.Frame(card, bg=PANEL_BG)
chk_panel.pack(fill="x", padx=32, pady=(0, 8), ipadx=8, ipady=5)

var_upper, var_lower, var_digits, var_symbols = tk.BooleanVar(value=True), tk.BooleanVar(value=True), tk.BooleanVar(
    value=True), tk.BooleanVar(value=True)
var_exclude_ambig, var_prevent_rep = tk.BooleanVar(value=False), tk.BooleanVar(value=True)


def create_check(parent, var, label, hint=""):
    row = tk.Frame(parent, bg=PANEL_BG)
    row.pack(fill="x", padx=10, pady=2)
    tk.Checkbutton(row, variable=var, bg=PANEL_BG, activebackground=PANEL_BG, selectcolor=ENTRY_BG, fg=CHK_SEL, bd=0,
                   cursor="hand2").pack(side="left")
    tk.Label(row, text=label, font=chk_font, bg=PANEL_BG, fg=TEXT).pack(side="left")
    if hint:
        tk.Label(row, text=hint, font=("Segoe UI", 9), bg=PANEL_BG, fg=MUTED).pack(side="right", padx=(0, 4))


create_check(chk_panel, var_upper, "☑ Uppercase Letters", "A – Z")
create_check(chk_panel, var_lower, "☑ Lowercase Letters", "a – z")
create_check(chk_panel, var_digits, "☑ Numbers", "0 – 9")
create_check(chk_panel, var_symbols, "☑ Symbols", "! @ # $ %")

tk.Frame(chk_panel, bg=CARD_BG, height=1).pack(fill="x", pady=6, padx=10)

create_check(chk_panel, var_exclude_ambig, "☑ Exclude Ambiguous", "(0, O, I, l, 1)")
create_check(chk_panel, var_prevent_rep, "☑ Prevent Repeated Characters")

pwd_container = tk.Frame(card, bg=ENTRY_BG)
pwd_container.pack(pady=(10, 3))

password_var = tk.StringVar()
tk.Entry(
    pwd_container, textvariable=password_var, font=entry_font,
    width=28, justify="center", bd=0, bg=ENTRY_BG, fg=ENTRY_FG, readonlybackground=ENTRY_BG, state="readonly",
).pack(side="left", ipady=12, padx=(12, 0))

copy_icon_btn = tk.Button(
    pwd_container, text="📋", font=("Segoe UI Emoji", 12),
    bg=ENTRY_BG, fg=MUTED, activebackground=ENTRY_BG, activeforeground=TEXT,
    relief="flat", bd=0, cursor="hand2", command=copy_password
)
copy_icon_btn.pack(side="right", padx=(0, 8), ipady=8)

copy_status_var = tk.StringVar(value="")
tk.Label(card, textvariable=copy_status_var, font=("Segoe UI", 9, "bold"), bg=CARD_BG, fg=CHK_SEL).pack(pady=(0, 6))

info_frame = tk.Frame(card, bg=PANEL_BG)
info_frame.pack(fill="x", padx=32, pady=(0, 12), ipadx=10, ipady=8)


def add_info_row(parent, label_text):
    row = tk.Frame(parent, bg=PANEL_BG)
    row.pack(fill="x", pady=2)
    tk.Label(row, text=label_text, font=label_font, bg=PANEL_BG, fg=MUTED).pack(side="left")
    val_label = tk.Label(row, text="--", font=strength_font, bg=PANEL_BG, fg=TEXT)
    val_label.pack(side="right")
    return val_label


lbl_strength_val = add_info_row(info_frame, "Strength:")
lbl_entropy_val = add_info_row(info_frame, "Entropy:")
lbl_types_val = add_info_row(info_frame, "Character Types:")
lbl_policy_val = add_info_row(info_frame, "Active Policy:")

lbl_policy_val.config(text="Enterprise")  # Initial state

canvas_total_w = BAR_SEGMENTS * (BAR_W + BAR_GAP) - BAR_GAP
canvas_bar = tk.Canvas(card, width=canvas_total_w, height=BAR_H, bg=CARD_BG, highlightthickness=0)
canvas_bar.pack(pady=(0, 16))

for i in range(BAR_SEGMENTS):
    canvas_bar.create_rectangle(i * (BAR_W + BAR_GAP), 0, i * (BAR_W + BAR_GAP) + BAR_W, BAR_H, fill=BAR_EMPTY,
                                outline="")

generate_btn = tk.Button(
    card, text="  ⚡  Generate Password", font=button_font,
    bg=ACCENT, fg=TEXT, activebackground=ACCENT_HV, activeforeground=TEXT,
    relief="flat", bd=0, padx=24, pady=10, cursor="hand2", command=generate_password,
)
generate_btn.pack(pady=(0, 8))

tk.Label(root, text="Powered by Python · cryptographically secure", font=("Segoe UI", 8), bg=BG, fg=MUTED).pack(
    side="bottom", pady=8)

generate_password()
root.mainloop()
