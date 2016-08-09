#!/usr/bin/python
import unittest

from flask import current_app

from consensus_web import create_app, db


class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        #valor = current_app.config['TESTING']
        self.assertTrue(current_app.config['TESTING'])

    def test_get(self):
        app = self.app.test_client()
        response = app.get('/')
        self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    unittest.main()