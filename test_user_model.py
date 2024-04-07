""" User Model tests """

# run these tests like:
#
#    python -m unittest test_user_model.py

import os
from unittest import TestCase
from models import db, User

os.environ['DATABASE_URL'] = "postgresql:///test_everyday_news"

from app import app

db.drop_all()
db.create_all()

app.config['WTF_CSRF_ENABLED'] = False


class UserTestCase(TestCase):
    """Test user."""

    # def setUp(self):
    #     """Create test client, add sample data."""
    #     User.query.delete()


    def test_register_user(self):
        """Test that user can be registered."""
        user = User.register("testuser", "testpass", "testfirst", "testlast")
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.first_name, "testfirst")
        self.assertEqual(user.last_name, "testlast")

    def test_authenticate_user(self):
        """Test that user can be authenticated."""
        user = User.register("testuser1", "testpass1", "testfirst", "testlast")
        db.session.add(user)
        db.session.commit()
        self.assertEqual(user.username, "testuser1")
        user2 = User.authenticate(user.username, "testpass1")
        self.assertEqual(user2.username, "testuser1")
