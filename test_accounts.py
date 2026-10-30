import unittest
from accounts import AccountStore

PASSWORD = 'DemoPassphrase-2026'

class SecurityTests(unittest.TestCase):
    def setUp(self):
        self.store = AccountStore()
        self.store.register('learner', PASSWORD)

    def tearDown(self):
        self.store.close()

    def test_correct_password(self):
        self.assertTrue(self.store.authenticate('learner', PASSWORD))

    def test_wrong_password(self):
        self.assertFalse(self.store.authenticate('learner', 'WrongPassphrase-2026'))

    def test_unknown_account(self):
        self.assertFalse(self.store.authenticate('missing', PASSWORD))

    def test_sql_injection_does_not_bypass_login(self):
        self.assertFalse(self.store.authenticate("' OR 1=1 --", PASSWORD))
        self.assertTrue(self.store.authenticate('learner', PASSWORD))

    def test_invalid_usernames(self):
        for username in ['', 'ab', 'a'*31, "user'; DROP TABLE users;--", None]:
            with self.subTest(username=username):
                with self.assertRaises(ValueError):
                    self.store.register(username, PASSWORD)

    def test_password_length_bounds(self):
        for password in ['short', 'a'*129, None]:
            with self.subTest(password_type=type(password).__name__):
                with self.assertRaises(ValueError):
                    self.store.register('another', password)

    def test_duplicate_rejected(self):
        with self.assertRaises(ValueError):
            self.store.register('learner', PASSWORD)

    def test_password_is_not_stored_as_plaintext(self):
        salt, digest = self.store.db.execute('SELECT salt, digest FROM users').fetchone()
        self.assertEqual(len(salt), 16)
        self.assertEqual(len(digest), 32)
        self.assertNotEqual(digest, PASSWORD.encode())

    def test_same_password_has_different_salt_and_digest(self):
        self.store.register('another', PASSWORD)
        rows = self.store.db.execute('SELECT salt, digest FROM users ORDER BY username').fetchall()
        self.assertNotEqual(rows[0][0], rows[1][0])
        self.assertNotEqual(rows[0][1], rows[1][1])

    def test_non_string_login_input_rejected(self):
        for username, password in [(None, PASSWORD), ('learner', None), (42, PASSWORD)]:
            with self.subTest(username=username):
                self.assertFalse(self.store.authenticate(username, password))

if __name__ == '__main__':
    unittest.main()
