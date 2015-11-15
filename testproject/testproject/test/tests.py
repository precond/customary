# coding=utf-8

from __future__ import unicode_literals

import json

from django.test import TestCase, Client
from django.utils.datetime_safe import datetime
from django.utils.timezone import UTC

from customary.api.models import ApiUser, ApiToken


class TestApiBase(TestCase):

    def setUp(self):
        self.api_user = ApiUser.objects.create(comment="API test user")
        self.token = ApiToken.objects.create(api_user=self.api_user, token='1234567890')

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

    def test_status(self):
        c = Client()
        start_time = datetime.now(tz=UTC())
        self.api_post(c, '/api/status/', data={'token': '1234567890'})
        token = ApiToken.objects.get(id=self.token.id)
        self.assertTrue(token.last_seen >= start_time)

    def test_status_get(self):
        c = Client()
        start_time = datetime.now(tz=UTC())
        self.api_get(c, '/api/status/?token=1234567890')
        token = ApiToken.objects.get(id=self.token.id)
        self.assertTrue(token.last_seen >= start_time)

    def test_status_invalid_token(self):
        self.token.delete()
        c = Client()
        self.api_post(c, '/api/status/', data={'token': '1234567890'}, expected_code=403, expected_message='Valid token required')

    def test_status_invalid_method(self):
        c = Client()
        response, data = self.api_put(c, '/api/status/', data={'token': '1234567890'}, expected_code=405, expected_message='Method not supported')
        self.assertEqual(response['Allow'], 'GET, POST')
