from django.conf import settings
import logging,uuid,traceback
from django.http import JsonResponse
from utils.custom_log_writer import log
from .views import get_tokens_for_user
logger = logging.getLogger("ReaderLogger")


class LoginRedirectCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        

        response = self.get_response(request)
        if request.path == '/redirect-to-front/' and request.user.is_authenticated:
            d = get_tokens_for_user(request.user)
            response.set_cookie("access",d[0],"",max_age=100)
            response.set_cookie("refresh",d[1],"",max_age=100)
        else:
            response.set_cookie("access","","", max_age=100)
            response.set_cookie("refresh","","",max_age=100)
        #response["access"] = "12312"
        # Code to be executed for each request/response after
        # the view is called.

        return response


class reqObj(object):
    method = ""
    user = ""
    host = ""
    path = ""


    def __init__(self, kwargs):
        self.method = kwargs["REQUEST_METHOD"]
        self.host = kwargs["HTTP_HOST"]
        self.path = kwargs["PATH_INFO"]
        
    def get_host(self):
        return self.host