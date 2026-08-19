import customtkinter as ctk
import random as random
import string as string
SYMBOLS = "!@#$%^&*()-_=+[]{};:'\",.<>?/\\|"

app = ctk.CTk()

app.title("Password Strength Checker")
app.geometry("400x600")

# Analyzes the inputed/generated password whether it has a number, uppercase, lowercase, and symbol.
def analyze_password(password):
    results = {
        "number": False,
        "uppercase": False,
        "lowercase": False,
        "symbol": False,
        "length": False
    }

    for character in password:
        if character.isdigit():
            results["number"] = True

        if character.isupper():
            results["uppercase"] = True

        if character.islower():
            results["lowercase"] = True

        if character in SYMBOLS:
            results["symbol"] = True

        if results["number"] and results["uppercase"] and results["lowercase"] and results["symbol"]:
            break

    return results

# Calculates the score of the inputed/generated password from 1 to 5.
def calculate_score(results):
    score = 0

    for passed in results.values():
        if passed: 
            score += 1

    return score

# Gets the strength result of the inputed/generated password and changes the text color based on the score. 
def get_strength(score):
    if score <= 2:
        return "Weak", "red"

    elif score == 3:
        return "Fair", "orange"

    elif score == 4:
        return "Good", "green"

    else:
        return "Excellent", "blue"

# Hides or shows the inputed/generated password. Changes the button's text accordingly.
def toggle_password():
    if password_entry.cget("show") == "*":
        password_entry.configure(show="")
        toggle_button.configure(text="Hide")
    else:
        password_entry.configure(show="*")
        toggle_button.configure(text="Show")

# Generates a random password with atleast one lowercase, uppercase, number, and symbol depending on the password length (4 to 32).
def generate_password(length):
    if length < 4:
        return ""

    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    numbers = string.digits
    symbols = SYMBOLS

    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(numbers),
        random.choice(symbols)
    ]

    characters = lowercase + uppercase + numbers + symbols

    for _ in range(length - 4):
        password.append(random.choice(characters))

    random.shuffle(password)

    return "".join(password)

# Shows the results of the analysis: progress bar, score, and advise for a better password.
def check_password():
    password = password_entry.get()

    results = analyze_password(password)
    results["length"] = len(password) >= 8

    score = calculate_score(results)

    strength, color = get_strength(score)

    progress_bar.configure(
        progress_color=color
    )

    score_label.configure(
        text=f"Score: {score} / 5"
    )

    progress_bar.set(score / 5)

    feedback_messages = {
        "length": "Use at least 8 characters.",
        "number": "Add at least 1 number.",
        "uppercase": "Add at least 1 uppercase letter.",
        "lowercase": "Add at least 1 lowercase letter.",
        "symbol": "Add at least 1 symbol."
    }

    feedback = []

    for rule, message in feedback_messages.items():
        if not results[rule]:
            feedback.append(message)

    if len(feedback) == 0:
        result = f"{strength}\n\nAll requirements met!"
    else:
        result = f"{strength}\n\n" + "\n".join(feedback)

    result_label.configure(
        text=result,
        text_color=color
    )

# Changes the password length based on the password generator slider.
def update_length_label(value):
    length = int(float(value))
    password_length.set(length)
    length_label.configure(
        text=f"Password Length: {length}"
    )

# Connects the "Generate Password" button to the generate_password function.
def generate_password_button():
    length = password_length.get()
    password = generate_password(length)

    password_entry.delete(0, "end")
    password_entry.insert(0, password)

# UI Elements of the Password Strength checker section.
strength_label = ctk.CTkLabel(
    app,
    text="Password Strength Checker",
    font=("Arial", 22, "bold")
)
strength_label.pack(pady=10)

password_entry = ctk.CTkEntry(
    app, 
    placeholder_text="Enter Password", 
    show="*"
)
password_entry.pack(pady=10, padx=25, fill="x")

toggle_button = ctk.CTkButton(
    app,
    text="Show",
    width=50,
    command=toggle_password
)
toggle_button.pack(pady=10)

check_button = ctk.CTkButton(
    app,
    text = "Check Password",
    width=125,
    command=check_password
)
check_button.pack(pady=10)

score_label = ctk.CTkLabel(
    app,
    text="Score: 0 / 5"
)
score_label.pack(pady=10)

progress_bar = ctk.CTkProgressBar(
    app,
    width=340
)
progress_bar.set(0)
progress_bar.pack(pady=10)

result_label = ctk.CTkLabel(
    app, 
    text=""
)
result_label.pack(pady=10)

# UI Elements of the Password Generator section.
generator_label = ctk.CTkLabel(
    app,
    text="Password Generator",
    font=("Arial", 22, "bold")
)
generator_label.pack(pady=10)

password_length = ctk.IntVar(value=12)

length_label = ctk.CTkLabel(
    app,
    text="Password Length: 12"
)
length_label.pack(pady=10)

length_slider = ctk.CTkSlider(
    app,
    from_=4,
    to=32,
    number_of_steps=28,
    variable=password_length,
    width=350,
    command=update_length_label
)
length_slider.pack(pady=10)

generate_button = ctk.CTkButton(
    app,
    text="Generate Password",
    width=140,
    command=generate_password_button
)
generate_button.pack(pady=10)

app.mainloop()