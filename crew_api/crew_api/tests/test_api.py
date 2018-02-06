from flask_testing import TestCase
from crew_api import app, db, TestConfig
from crew_api.models import metadata, AttrInItem, FeeLog, ItemAttribute, Member

import unittest

class BaseTestCase(TestCase):
    """A base test case."""

    def create_app(self):
        app.config.from_object(TestConfig)
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

if __name__ == '__main__':
    unittest.main()