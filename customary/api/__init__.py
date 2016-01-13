# coding=utf-8

from __future__ import unicode_literals

import json
import logging

from functools import wraps

from django.apps import apps
from django.http import JsonResponse
from django.utils.decorators import available_attrs


DEFAULT_API_METHODS = ['PUT', 'GET', 'POST', 'DELETE']

logger = logging.getLogger('customary.api')


def api_request(methods=None, require_token=True):
    """
    View decorator that handles JSON based API requests and responses consistently.
    :param methods: A list of allowed methods
    :param require_token: Whether API token is checked automatically or not
    """
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            ApiToken = apps.get_model('api', 'ApiToken')
            m = methods if methods is not None else DEFAULT_API_METHODS
            if request.method not in m:
                response = ApiResponse(False, 'Method not supported', status=405)
                response['Allow'] = ', '.join(methods)
                return response

            try:
                data = json.loads(request.body.decode('utf-8')) if request.body else {}
                if require_token:
                    token_string = request.GET['token'] if request.method == 'GET' else data['token']
                    try:
                        token = ApiToken.objects.get(token=token_string)
                        token.save()  # Update the last_seen field
                        data['token'] = token

                    except ApiToken.DoesNotExist:
                        logger.exception('Valid token required, "{0}" supplied'.format(token_string))
                        return ApiResponse(False, 'Valid token required', status=403)

                return ApiResponse(data=view_func(request, data=data, *args, **kwargs))

            except Exception as e:
                if e.__class__.__name__ == 'DoesNotExist':
                    logger.exception('Not found while handling ajax request')
                    return ApiResponse(False, 'Exception: {0}'.format(e), status=404)
                else:
                    logger.exception('Error handling ajax request')
                    return ApiResponse(False, 'Exception: {0}'.format(e), status=500)

        return _wrapped_view
    return decorator


class ApiResponse(JsonResponse):
    def __init__(self, success=True, message=None, data=None, *args, **kwargs):
        data = dict() if data is None else data
        data['success'] = success
        if message:
            data['message'] = message
        super(ApiResponse, self).__init__(data=data, safe=True, *args, **kwargs)
