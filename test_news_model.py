""" User Model tests """

# run these tests like:
#
#    python -m unittest test_news_model.py

import os
from unittest import TestCase
from models import db, News

os.environ['DATABASE_URL'] = "postgresql:///test_everyday_news"

from app import app

db.drop_all()
db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class NewsViewTestCase(TestCase):

    def test_news(self):
        """Test that news can be added."""
        news = News(author="testauthor", title="testtitle", description="testdescription", url="testurl", image_url="testurlToImage", publisedAt='2024-04-04 00:00', content="testcontent")

        db.session.add(news)
        db.session.commit()

        self.assertEqual(news.author, "testauthor")
