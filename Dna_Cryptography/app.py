from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os

app = Flask(__name__)
app.secret_key = "ammubhava"

def encrypt(user_input, dna_data):
    encrypted_result = []
    for char in user_input:
        if char in dna_data.values():
            encrypted_result.append(list(dna_data.keys())[list(dna_data.values()).index(char)])
        else:
            encrypted_result.append(char)
    return ''.join(str(s) for s in encrypted_result)

def decrypt(user_input, dna_data):
    user_input = user_input.replace(" ", "")
    user_input = user_input.rstrip()
    decrypted_result = []
    for i in range(0, len(user_input), 3):
        triplet = user_input[i:i + 3]
        decrypted_result.append(dna_data.get(triplet, triplet))
    decrypted_text = ''.join(decrypted_result)
    return decrypted_text

def load_dna_data(file_path):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: DNA data file not found.")
        return {}
    except json.JSONDecodeError:
        print("Error: Invalid JSON data.")
        return {}

def load_user_data(file_path):
    try:
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                return json.load(f)
        else:
            print("User data file not found. Creating a new one.")
            with open(file_path, "w") as f:
                json.dump({}, f)
            return {}
    except Exception as e:
        print(f"Error: {e}")
        return {}

def save_user_data(file_path, user_data):
    with open(file_path, "w") as f:
        json.dump(user_data, f, indent=4)

def authenticate_user(username, password, user_data):
    if username in user_data and user_data[username]["password"] == password:
        return True
    return False

def signup_user(username, password, user_data):
    if username in user_data:
        flash("Username already exists.", "error")
        return False
    user_data[username] = {"password": password}
    save_user_data("users.json", user_data)
    flash("User registered successfully!", "success")
    return True

@app.route("/home")
def welcome():
    return render_template("home.html")

@app.route("/")
def home():
    return redirect(url_for("signup_page"))

@app.route("/signup", methods=["GET", "POST"])
def signup_page():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user_data = load_user_data("users.json")
        if signup_user(username, password, user_data):
            return redirect(url_for("login"))
    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user_data = load_user_data("users.json")
        if authenticate_user(username, password, user_data):
            session["username"] = username
            return redirect(url_for("welcome"))
        else:
            flash("Invalid username or password.", "error")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

@app.route("/encrypt", methods=["GET", "POST"])
def encrypt_text():
    if "username" in session:
        if request.method == "POST":
            user_input = request.form["text"]
            dna_data = load_dna_data("dna.json")
            encrypted_result = encrypt(user_input, dna_data)
            return render_template("encryption.html", encrypted_result=encrypted_result)
        return render_template("encryption.html")
    return redirect(url_for("login"))

@app.route("/decrypt", methods=["GET", "POST"])
def decrypt_text():
    if "username" in session:
        if request.method == "POST":
            user_input = request.form["text"]
            dna_data = load_dna_data("dna.json")
            decrypted_result = decrypt(user_input, dna_data)
            return render_template("decryption.html", decrypted_result=decrypted_result)
        return render_template("decryption.html")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
