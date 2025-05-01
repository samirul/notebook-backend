import json
from django.utils.deprecation import MiddlewareMixin
from notebook.settings import REST_AUTH

class MoveJWTRefreshCookieIntoTheBody(MiddlewareMixin):
    """Middleware for moving refresh_token from header to body
    as required by dj_rest_auth for refresh token to get new access_token"""

    def __init__(self, get_response):
        super().__init__(get_response)
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)
    
    def process_view(self, request, view_func, *view_args, **view_kwargs):
        """process_view is called after Django determines which view will handle the request,
        but before that view is called. It will have access to the request object,
        along with the view that will handle it and the parameters that will be passed to that view."""
        
        if request.path == '/token/refresh/' and REST_AUTH.get('JWT_AUTH_REFRESH_COOKIE') in request.COOKIES:
            if request.body != b'':
                data = json.loads(request.body)
                data['refresh'] = request.COOKIES[REST_AUTH.get('JWT_AUTH_REFRESH_COOKIE')]
                request._body = json.dumps(data).encode('utf-8')
            else:
                pass
        
        return None