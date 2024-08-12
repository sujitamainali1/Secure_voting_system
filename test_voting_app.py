import unittest
import sqlite3
from cryptography.fernet import Fernet
from voting_app import register_user, login_user, cast_vote, tally_votes

# Load the encryption key
with open('secret.key', 'rb') as key_file:
    key = key_file.read()
cipher_suite = Fernet(key)

class TestVotingSystem(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create an in-memory SQLite database for testing
        cls.conn = sqlite3.connect(':memory:')
        cls.c = cls.conn.cursor()

        # Create the users and votes tables
        cls.c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password BLOB,
                age TEXT,
                nationality TEXT,
                gender TEXT
            )
        ''')
        cls.c.execute('''
            CREATE TABLE IF NOT EXISTS votes (
                username TEXT,
                vote TEXT
            )
        ''')
        cls.conn.commit()

    @classmethod
    def tearDownClass(cls):
        # Close the connection to the database
        cls.conn.close()

    def setUp(self):
        # Clear the tables before each test
        self.c.execute('DELETE FROM users')
        self.c.execute('DELETE FROM votes')
        self.conn.commit()

    def test_register_user(self):
        # Test user registration
        result = register_user('a3', 'newpass', '25', 'Country', 'Female')
        self.assertTrue(result)

        # Verify the user is actually in the database
        conn = sqlite3.connect('votes.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ?', ('a3',))
        user = c.fetchone()
        conn.close()

        self.assertIsNotNone(user, "User was not registered successfully")


    def test_login_user(self):
        # Register a user
        register_user('b3', 'password123', '25', 'Country', 'Male')

        # Test login with correct credentials
        result = login_user('b3', 'password123')


        # Test login with incorrect password
        result = login_user('b3', 'wrongpassword')
        self.assertFalse(result)

        # Test login with non-existent user
        result = login_user('c3', 'password123')
        self.assertFalse(result)



    def test_cast_vote(self):
        # Register a user
        register_user('suju', 'password123', '25', 'Country', 'Male')

        # Log in the user
        login_result = login_user('suju', 'password123')
        self.assertTrue(login_result, "Login should be successful")

        # Cast a vote
        cast_vote('suju', 'Candidate A')

        # Verify the vote is recorded correctly
        conn = sqlite3.connect('votes.db')
        c = conn.cursor()

        # Check if the votes table exists and has any data
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='votes';")
        table_exists = c.fetchone()
        print("Votes table exists:", table_exists)

        c.execute('SELECT * FROM votes')
        all_votes = c.fetchall()
        print("All votes in the database:", all_votes)
        conn.close()

    def test_tally_votes(self):
        register_user('e3', 'pass1')
        register_user('f3', 'pass2')
        cast_vote('e3', 'KP Sharma Oli')
        cast_vote('f3', 'Pushpa Kamal Dahal')
        
        results = tally_votes(gui_mode=False)
        self.assertEqual(len(results), 2, "Tally results count mismatch")

if __name__ == '__main__':
    unittest.main()
