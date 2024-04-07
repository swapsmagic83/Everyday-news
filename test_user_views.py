""" User Model tests """

# run these tests like:
#
#    python -m unittest test_user_views.py

import os
from unittest import TestCase
from models import db, User, News, Vote, Favorite

os.environ['DATABASE_URL'] = "postgresql:///test_everyday_news"

from app import app

db.drop_all()
db.create_all()

app.config['WTF_CSRF_ENABLED'] = False


class UserViewTestCase(TestCase):
    """Test views for user."""

    def setUp(self):
        """Create test client, add sample data."""
        Vote.query.delete()
        Favorite.query.delete()
        User.query.delete()
        News.query.delete()

        self.client = app.test_client()
        self.user = User.register("testuser", "testpass", "testfirst", "testlast")
        db.session.add(self.user)
        db.session.commit()

        self.news = News(author="testauthor", title="testtitle", description="testdescription", url="testurl", image_url="testurlToImage", publisedAt='2024-04-04 00:00', content="testcontent")

        db.session.add(self.news)
        db.session.commit()


    def test_get_user(self):
        """Test that user can be signed up."""
        with self.client as c:
            with c.session_transaction() as sess:
                sess['username'] = self.user.username

            resp = self.client.get(f"/users/{self.user.username}")
            self.assertEqual(resp.status_code, 200)

            self.assertIn(b"testuser", resp.data)

    def test_user_new_favorite(self):
        """Test add new user favorite news."""
        with self.client as c:
            with c.session_transaction() as sess:
                sess['username'] = self.user.username

            resp = self.client.post(f"/users/{self.user.username}/new-favorite", data={"newsid": self.news.id})
            self.assertEqual(resp.status_code, 302)

            self.assertIn(b"testuser", resp.data)

            self.assertEqual(len(self.user.favorites), 1)
            self.assertEqual(self.user.favorites[0].news_id, self.news.id)

    def test_user_news_vote(self):
        """Test user can vote on news."""
        with self.client as c:
            with c.session_transaction() as sess:
                sess['username'] = self.user.username

            resp = self.client.post(f"/users/{self.user.username}/vote", data={"newsid": self.news.id})
            self.assertEqual(resp.status_code, 302)

            self.assertIn(b"testuser", resp.data)

            self.assertEqual(len(self.news.vote), 1)
            self.assertEqual(self.news.vote[0].user_id, self.user.id)
