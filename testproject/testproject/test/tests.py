# coding=utf-8

from __future__ import unicode_literals, print_function

import json

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.utils.datetime_safe import datetime
from django.utils.timezone import UTC

from customary.api.models import ApiUser, ApiToken


class TestApiBase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('user1', 'user@users.com', 'user1', first_name='User1', last_name='User')
        self.api_user = ApiUser.objects.create(user=self.user, comment='API test user1')
        self.token = ApiToken.objects.create(api_user=self.api_user, token='1234567890', comment='Status token 1')
        self.api_user2 = ApiUser.objects.create(comment='API test user2')
        self.token2 = ApiToken.objects.create(api_user=self.api_user2, token='0987654321', comment='Status token 2')

    def api_post(self, c, url, data, expected_code=200, expected_message=None):
        do_request = lambda: c.post(url, data=json.dumps(data), content_type='application/json', follow=True)
        return self.make_api_request(do_request, expected_code, expected_message)

    def api_put(self, c, url, data, expected_code=200, expected_message=None):
        do_request = lambda: c.put(url, data=json.dumps(data), content_type='application/json', follow=True)
        return self.make_api_request(do_request, expected_code, expected_message)

    def api_delete(self, c, url, data, expected_code=200, expected_message=None):
        do_request = lambda: c.delete(url, data=json.dumps(data), content_type='application/json', follow=True)
        return self.make_api_request(do_request, expected_code, expected_message)

    def api_get(self, c, url, expected_code=200, expected_message=None):
        do_request = lambda: c.get(url, follow=True)
        return self.make_api_request(do_request, expected_code, expected_message)

    def make_api_request(self, do_request, expected_code=200, expected_message=None):
        response = do_request()
        self.assertEqual(response.status_code, expected_code)
        reply = json.loads(response.content.decode('utf-8'))
        if expected_code >= 400:
            self.assertFalse(reply['success'])
        else:
            self.assertTrue(reply['success'])
        if expected_message:
            self.assertEqual(reply['message'], expected_message)
        return response, reply


class TestApiCore(TestApiBase):

    def test_apiuser_str(self):
        self.assertEqual(str(self.api_user), 'user1 (API test user1)')
        self.assertEqual(str(self.api_user2), 'API test user2')

    def test_apitoken_str(self):
        self.assertEqual(str(self.token), 'user1 (Status token 1)')
        self.assertEqual(str(self.token2), 'API test user2 (Status token 2)')

    def test_status(self):
        c = Client()
        start_time = datetime.now(tz=UTC())
        self.api_post(c, '/api/status/', data={'token': self.token.token})
        token = ApiToken.objects.get(id=self.token.id)
        self.assertTrue(token.last_seen >= start_time)

    def test_status_get(self):
        c = Client()
        start_time = datetime.now(tz=UTC())
        self.api_get(c, '/api/status/?token={0}'.format(self.token.token))
        token = ApiToken.objects.get(id=self.token.id)
        self.assertTrue(token.last_seen >= start_time)

    def test_status_invalid_token(self):
        self.token.delete()
        c = Client()
        self.api_post(c, '/api/status/', data={'token': self.token.token}, expected_code=403, expected_message='Valid token required')

    def test_status_invalid_method(self):
        c = Client()
        response, data = self.api_put(c, '/api/status/', data={'token': self.token.token}, expected_code=405, expected_message='Method not supported')
        self.assertEqual(response['Allow'], 'GET, POST')
