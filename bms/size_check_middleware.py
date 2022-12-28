from django.conf import settings
from .serializers import GenericResponse, GenericResponseSerializer
import logging,uuid,traceback
from django.http import JsonResponse
from utils.custom_log_writer import log
logger = logging.getLogger("ReaderLogger")


class SizeCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        print("hi")
        try:
            size = int(request.META.get('CONTENT_LENGTH')) if request.META.get('CONTENT_LENGTH') != '' else 0
            if size > settings.DATA_UPLOAD_MAX_MEMORY_SIZE:
                raise Exception("Upload size too big")
        except Exception as ex:
            _id = str(uuid.uuid4())
            req = reqObj(request.META)
            log(req, _id, "File too big", "",None )
            logger.info("POST: {} | ID: {} | HOST: {} data: {}".format(request.path,_id, request.get_host(), "data too long"))
            responseObject = GenericResponse(_id=_id, status="-3",errorMessage=[str(ex)])
            response=GenericResponseSerializer(responseObject)
            log(req, _id, "File too big", response.data,traceback.format_exc())
            return JsonResponse(response.data, status=400)

        response = self.get_response(request)

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