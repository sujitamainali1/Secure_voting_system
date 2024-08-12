import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet
import sqlite3
from PIL import Image, ImageTk

# #  Generate and save a key for encryption/decryption 
key = Fernet.generate_key()
cipher_suite = Fernet(key)
# Save the key to a file 
with open('secret.key', 'wb') as key_file:
    key_file.write(key)

# Load the key from the file
with open('secret.key', 'rb') as key_file:
    key = key_file.read()
cipher_suite = Fernet(key)


# Connect to the database
conn = sqlite3.connect('votes.db')
c = conn.cursor()

# Create the tables if they do not exist
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password BLOB,
    age TEXT,
    nationality TEXT,
    gender TEXT
    )
''')
c.execute('''
    CREATE TABLE IF NOT EXISTS votes (
        username TEXT,
        vote TEXT
    )
''')
conn.commit()

def register_user(username, password, age='', nationality='', gender=''):
    encrypted_password = cipher_suite.encrypt(password.encode())
    try:
        c.execute('INSERT INTO users (username, password, age, nationality, gender) VALUES (?, ?, ?, ?, ?)', 
                  (username, encrypted_password, age, nationality, gender))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def login_user(username, password):
    c.execute('SELECT password FROM users WHERE username = ?', (username,))
    result = c.fetchone()
    if result:
        encrypted_password = result[0]
        try:
            decrypted_password = cipher_suite.decrypt(encrypted_password).decode()
            if decrypted_password == password:
                return True
        except:
            pass
    return False

def cast_vote(username, vote):
    c.execute('INSERT INTO votes (username, vote) VALUES (?, ?)', (username, vote))
    conn.commit()

def tally_votes():
    c.execute('SELECT vote, COUNT(*) FROM votes GROUP BY vote')
    return c.fetchall()

# Initialize the Tkinter window
root = tk.Tk()
root.title("Secure Voting System")
root.geometry("600x570")  # Adjusted dimensions
root.configure(bg='lightgrey')

# Global variable to store current username
current_username = None

# Function to switch to a specific frame
def show_frame(frame):
    frame.tkraise()
    if frame == vote_frame and current_username is None:
        messagebox.showerror("Error", "You must be logged in to access this page.")
        show_frame(home_frame)

# Create Frames
def create_home_frame():
    home_frame = tk.Frame(root, bg='lightgrey')
    home_frame.grid(row=0, column=0, sticky='nsew')
    # Load the image
    image_path = 'home_image.png' 
    image = Image.open(image_path)
    image = image.resize((300, 200), Image.LANCZOS) 
    photo = ImageTk.PhotoImage(image)
    image_label = tk.Label(home_frame, image=photo, bg='lightgrey')
    image_label.image = photo 
    image_label.pack(pady=20)
    button_frame = tk.Frame(home_frame, bg='lightgrey')
    button_frame.pack(pady=20)
    tk.Button(button_frame, text="Login", command=lambda: show_frame(login_frame), 
              font=("Arial", 14), bg='blue', fg='white').pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="Register", command=lambda: show_frame(register_frame), 
              font=("Arial", 14), bg='green', fg='white').pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="Cast Vote", command=lambda: show_frame(vote_frame), 
              font=("Arial", 14), bg='red', fg='white').pack(side=tk.LEFT, padx=10)
    tk.Label(home_frame, text="Welcome to the Secure Voting System!!",
              font=("Arial", 24), bg='lightgrey').pack(pady=20)
    return home_frame


def create_login_frame():
    global username_entry_login, password_entry_login

    login_frame = tk.Frame(root, bg='lightgrey')
    login_frame.grid(row=0, column=0, sticky='nsew')

    tk.Label(login_frame, text="Login", font=("Arial", 18), bg='lightgrey').pack(pady=10)

    tk.Label(login_frame, text="Username:", font=("Arial", 12), bg='lightgrey').pack(pady=5)
    username_entry_login = tk.Entry(login_frame, font=("Arial", 12))
    username_entry_login.pack(pady=5)

    tk.Label(login_frame, text="Password:", font=("Arial", 12), bg='lightgrey').pack(pady=5)
    password_entry_login = tk.Entry(login_frame, font=("Arial", 12), show='*')
    password_entry_login.pack(pady=5)

    tk.Button(login_frame, text="Login", command=login, 
        font=("Arial", 12), bg='blue', fg='white').pack(pady=10)
    tk.Button(login_frame, text="Back to Home", 
        command=lambda: show_frame(home_frame), font=("Arial", 12), bg='grey',
              fg='white').pack(pady=10)
    return login_frame

def create_register_frame():
    global username_entry_register, password_entry_register, age_entry, nationality_entry, gender_var

    register_frame = tk.Frame(root, bg='lightgrey')
    register_frame.grid(row=0, column=0, sticky='nsew')

    tk.Label(register_frame, text="Register", font=("Arial", 24), bg='lightgrey').pack(pady=20)

    tk.Label(register_frame, text="Username:", font=("Arial", 14), bg='lightgrey').pack(pady=5)
    username_entry_register = tk.Entry(register_frame, font=("Arial", 14))
    username_entry_register.pack(pady=5)

    tk.Label(register_frame, text="Password:", font=("Arial", 14), bg='lightgrey').pack(pady=5)
    password_entry_register = tk.Entry(register_frame, font=("Arial", 14), show='*')
    password_entry_register.pack(pady=5)

    tk.Label(register_frame, text="Age:", font=("Arial", 14), bg='lightgrey').pack(pady=5)
    age_entry = tk.Entry(register_frame, font=("Arial", 14))
    age_entry.pack(pady=5)

    tk.Label(register_frame, text="Nationality:", font=("Arial", 14), bg='lightgrey').pack(pady=5)
    nationality_entry = tk.Entry(register_frame, font=("Arial", 14))
    nationality_entry.pack(pady=5)

    tk.Label(register_frame, text="Gender:", font=("Arial", 14), bg='lightgrey').pack(pady=5)
    gender_var = tk.StringVar(value="Select")  # Default value.
    gender_options = ["Select", "Male", "Female", "Other"]
    gender_menu = tk.OptionMenu(register_frame, gender_var, *gender_options)
    gender_menu.config(font=("Arial", 14))
    gender_menu.pack(pady=5)

    tk.Button(register_frame, text="Register", command=register, 
              font=("Arial", 14), bg='blue', fg='white').pack(pady=10)
    tk.Button(register_frame, text="Back to Home", command=lambda: show_frame(home_frame), 
              font=("Arial", 14), bg='grey', fg='white').pack(pady=10)

    return register_frame

def create_vote_frame():
    global vote_var, candidate_photos  # Declare candidate_photos as global

    vote_var = tk.StringVar()
    candidate_photos = []  # List to keep references to images

    vote_frame = tk.Frame(root, bg="#f0f0f0")
    vote_frame.grid(row=0, column=0, sticky='nsew')

    tk.Label(vote_frame, text="Choose a candidate to vote for:", 
        font=("Arial", 16), bg="#f0f0f0", fg="#333").pack(pady=20)

    # Candidate images and names
    candidates = [
        ('candidate1.jpeg', 'KP Sharma Oli'),
        ('candidate2.jpeg', 'Pushpa Kamal Dahal'),
        ('candidate3.jpeg', 'Balen Shah')
    ]

    # Create a frame for candidates
    candidates_frame = tk.Frame(vote_frame, bg="#f0f0f0")
    candidates_frame.pack()

    # Use grid to arrange candidates side by side
    row = 0
    column = 0
    for image_path, name in candidates:
        # Load and resize image
        image = Image.open(image_path)
        image = image.resize((100, 100), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        candidate_photos.append(photo)  # Keep reference to the image

        # Create frame for each candidate
        candidate_frame = tk.Frame(candidates_frame, bg="#f0f0f0")
        candidate_frame.grid(row=row, column=column, padx=10, pady=10)

        tk.Label(candidate_frame, image=photo, bg="#f0f0f0").pack()
        tk.Label(candidate_frame, text=name, font=("Arial", 14), bg="#f0f0f0").pack()

        tk.Radiobutton(candidate_frame, text=name, variable=vote_var, 
            value=name, font=("Arial", 14), bg="#f0f0f0").pack()

        # Move to the next column
        column += 1
        if column > 2:  # Number of columns per row
            column = 0
            row += 1

    tk.Button(vote_frame, text="Cast Vote", command=cast_vote, 
        font=("Arial", 14), bg="#4CAF50", fg="#fff").pack(pady=20)
    tk.Button(vote_frame, text="Tally Votes", command=tally_votes,
        font=("Arial", 14), bg="#2196F3", fg="#fff").pack(pady=20)
    tk.Button(vote_frame, text="Logout", command=logout, 
        font=("Arial", 14), bg="#f44336", fg="#fff").pack(pady=10)

    return vote_frame


# GUI Functions
def register():
    username = username_entry_register.get()
    password = password_entry_register.get()
    age = age_entry.get()
    nationality = nationality_entry.get()
    gender = gender_var.get()

    if not username or not password or gender == "Select":
        messagebox.showerror("Error", "Please fill in all required fields.")
        return

    encrypted_password = cipher_suite.encrypt(password.encode())

    try:
        c.execute('INSERT INTO users (username, password, age, nationality, gender) VALUES (?, ?, ?, ?, ?)', 
                  (username, encrypted_password, age, nationality, gender))
        conn.commit()
        messagebox.showinfo("Success", "Registration successful!")
        show_frame(home_frame)
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists.")


def login():
    username = username_entry_login.get()
    password = password_entry_login.get()

    # Encrypt the entered password
    encrypted_password = cipher_suite.encrypt(password.encode())

    # Fetch the encrypted password from the database
    c.execute('SELECT password FROM users WHERE username=?', (username,))
    result = c.fetchone()

    if result:
        # Decrypt the password stored in the database
        stored_encrypted_password = result[0]
        try:
            print(f"Stored encrypted password: {stored_encrypted_password}")  # Debugging statement
            decrypted_password = cipher_suite.decrypt(stored_encrypted_password).decode()
            print(f"Decrypted password: {decrypted_password}")  # Debugging statement
            if decrypted_password == password:
                global current_username
                current_username = username
                messagebox.showinfo("Success", "Login successful!")
                show_frame(vote_frame)
            else:
                messagebox.showerror("Error", "Invalid username or password.")
        except Exception as e:
            print(f"Decryption error: {str(e)}")  # Debugging statement
            messagebox.showerror("Error", f"An error occurred during login: {str(e)}")
    else:
        messagebox.showerror("Error", "Invalid username or password.")

def cast_vote():
    if current_username is None:
        messagebox.showerror("Error", "You must be logged in to cast a vote.")
        return

    # Check if the user has already voted
    c.execute('SELECT * FROM votes WHERE username = ?', (current_username,))
    existing_vote = c.fetchone()
    
    if existing_vote:
        messagebox.showerror("Error", "You have already cast your vote.")
        return

    vote = vote_var.get()
    
    if not vote:
        messagebox.showerror("Error", "Please select a candidate.")
        return

    if vote not in ['KP Sharma Oli', 'Pushpa Kamal Dahal', 'Balen Shah']:
        messagebox.showerror("Error", "Invalid candidate.")
        return

    c.execute('INSERT INTO votes (username, vote) VALUES (?, ?)', (current_username, vote))
    conn.commit()

    messagebox.showinfo("Success", f"Vote for {vote} cast successfully!")


def tally_votes():
    # Fetch the vote counts from the database
    c.execute('SELECT vote, COUNT(*) FROM votes GROUP BY vote')
    results = c.fetchall()

    tally_window = tk.Toplevel(root)
    tally_window.title("Vote Tally")
    tally_window.geometry("300x300")  # Adjust size as needed

    # Create headings for the table
    tk.Label(tally_window, text="Candidates", 
        font=("Arial", 14, "bold")).grid(row=0, column=0, padx=10, pady=10)
    tk.Label(tally_window, text="Vote Count", 
        font=("Arial", 14, "bold")).grid(row=0, column=1, padx=10, pady=10)

        # Populate the table with vote counts
    for idx, (candidate, count) in enumerate(results):
        if candidate in ['KP Sharma Oli', 'Pushpa Kamal Dahal', 'Balen Shah']:
            tk.Label(tally_window, text=candidate, 
                font=("Arial", 12)).grid(row=idx + 1, column=0, padx=10, pady=5, sticky='w')
            tk.Label(tally_window, text=str(count),
                font=("Arial", 12)).grid(row=idx + 1, column=1, padx=10, pady=5, sticky='w')

            # Add a button to close the window
            tk.Button(tally_window, text="Close", command=tally_window.destroy, 
                font=("Arial", 12)).grid(row=len(results) + 1, columnspan=2, pady=10)
        else:
            return results


def logout():
    global current_username
    current_username = None
    username_entry_login.delete(0, tk.END) 
    password_entry_login.delete(0, tk.END) 
    show_frame(home_frame)


# Create frames
home_frame = create_home_frame()
login_frame = create_login_frame()
register_frame = create_register_frame()
vote_frame = create_vote_frame()

# Show the home frame initially
show_frame(home_frame)

root.mainloop()
