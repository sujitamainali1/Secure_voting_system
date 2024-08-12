Secure Voting System
This Python application provides a secure voting system implemented using Tkinter for the GUI, SQLite for database management, and cryptography for password encryption.

Features
Registration and Login: Users can register with a username, password, age, nationality, and gender. Existing usernames are checked for uniqueness.
Password Encryption: Uses Fernet encryption from the cryptography library to securely store passwords.
Voting: Registered users can cast votes for candidates displayed with images and names.
Vote Tally: Administrators can view the tally of votes for each candidate.
Session Management: Users must log in to access voting functionalities, ensuring security.

Dependencies
Python 3.x
tkinter
Pillow (PIL)
cryptography

Files
voting_app.py: Main application script.
secret.key: Stores the encryption key securely.
votes.db: SQLite database file containing user and vote data.

Installation
Ensure Python and the required libraries (tkinter, Pillow, cryptography) are installed.
Clone the repository or download the secure_voting_system.py script.
Run python secure_voting_system.py to start the application.

Usage
Registration: Fill in the required fields and click "Register" on the home screen.
Login: Enter your username and password to access voting features.
Voting: Select a candidate and click "Cast Vote". Only one vote per user is allowed.
Vote Tally: Click "Tally Votes" to view the current vote count for each candidate.
Logout: Users can log out to return to the home screen.

Notes
Ensure secret.key is kept secure as it contains the encryption key.
Modify candidate images (candidate1.jpeg, candidate2.jpeg, candidate3.jpeg) and their names as needed.
Customize GUI elements and functionality as per project requirements.
