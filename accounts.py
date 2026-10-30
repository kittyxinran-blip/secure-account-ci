"""Educational in-memory account store; not a production login service."""
import hashlib
import hmac
import re
import secrets
import sqlite3

ITERATIONS = 600_000

class AccountStore:
    def __init__(self):
        self.db = sqlite3.connect(':memory:')
        self.db.execute('CREATE TABLE users (username TEXT PRIMARY KEY, salt BLOB NOT NULL, digest BLOB NOT NULL)')

    def register(self, username, password):
        if not isinstance(username, str) or not re.fullmatch(r'[A-Za-z0-9_]{3,30}', username):
            raise ValueError('Username must contain 3-30 letters, digits or underscores')
        if not isinstance(password, str) or not 12 <= len(password) <= 128:
            raise ValueError('Password must contain 12-128 characters')
        salt = secrets.token_bytes(16)
        digest = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, ITERATIONS)
        try:
            self.db.execute('INSERT INTO users VALUES (?, ?, ?)', (username, salt, digest))
            self.db.commit()
        except sqlite3.IntegrityError as exc:
            raise ValueError('Account already exists') from exc

    def authenticate(self, username, password):
        if not isinstance(username, str) or len(username) > 128:
            return False
        if not isinstance(password, str) or not 12 <= len(password) <= 128:
            return False
        row = self.db.execute('SELECT salt, digest FROM users WHERE username = ?', (username,)).fetchone()
        if row is None:
            return False
        actual = hashlib.pbkdf2_hmac('sha256', password.encode(), row[0], ITERATIONS)
        return hmac.compare_digest(actual, row[1])

    def close(self):
        self.db.close()
