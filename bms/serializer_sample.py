from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    book_file = serializers.FileField(label="bookFile")

    class Meta:
        model = Book
        fields=["book_file"]

from rest_framework import serializers
from .models import UrlMasterModel
import datetime
import pytz
from django.conf import settings
from zoneinfo import ZoneInfo

class UrlSerializer(serializers.ModelSerializer):
    """
    Serializer for UrlMaster Model, Not in use
    """
    class Meta:
        model = UrlMasterModel
        fields =["finalUrl"]

class GenerateUrlRequestSerializer(serializers.Serializer):
    """"
    Serializer for generate url request
    """
    longUrl=serializers.URLField(required=True)
    source=serializers.CharField(max_length=100,required=True)
    expiry=serializers.DateTimeField(required=False,format="%Y-%m-%dT%H:%M:%S%z.")  

    def validate(self, data):
        today=datetime.datetime.now( pytz.UTC)
         # DEFAULT_EXPIRY= today+datetime.timedelta(days=settings.DEFAULT_EXPIRY_DAYS)
        # MAX_EXPIRY=today+datetime.timedelta(days=settings.MAX_EXPIRY_DAYS)
        DEFAULT_EXPIRY= datetime.datetime.strptime(settings.MAX_EXPIRY_DATE, "%d-%m-%Y").replace(tzinfo=pytz.UTC)
        MAX_EXPIRY=datetime.datetime.strptime(settings.MAX_EXPIRY_DATE, "%d-%m-%Y").replace(tzinfo=pytz.UTC)
        data['expiry']=self.need_24_expiry(data)
        userExpiry = data['expiry']

        if 'source' not in data:
            raise serializers.ValidationError("Source is required")
        if userExpiry > MAX_EXPIRY:
            raise serializers.ValidationError('Exipry too long')
        if userExpiry < today:
            raise serializers.ValidationError('Expiry too low')

        if len(data['longUrl'])>2000:
            raise serializers.ValidationError('Long Url too long')

        return data

    def need_24_expiry(self, data):
        if settings.EXPIRY24 == True:
            now = datetime.datetime.now(tz=ZoneInfo('Asia/Riyadh'))
            expiry = now + datetime.timedelta(hours = 24)
            return expiry
        else:
            DEFAULT_EXPIRY= datetime.datetime.strptime(settings.MAX_EXPIRY_DATE, "%d-%m-%Y").replace(tzinfo=pytz.UTC)
            return DEFAULT_EXPIRY if data.get('expiry',None) == None else data['expiry']

class GenericResponseSerializer(serializers.Serializer):
    """
    Default response serializer
    """
    success=serializers.CharField(max_length=5)
    errorId=serializers.CharField(max_length=5)
    errorMessage=serializers.CharField(max_length=200)
class GenerateUrlResponseSerializer(GenericResponseSerializer):
    """
    Generate URL response serialer
    """
    shortUrl=serializers.URLField()

class GenericResponse(object):
    """
    Default response object
    """
    def __init__(self,**kwargs):
        self.success=kwargs['success'] if 'success' in kwargs else '0'
        self.errorMessage=kwargs['errorMessage'] if 'errorMessage' in kwargs  else ''
        self.errorId=kwargs['errorId'] if 'errorId' in kwargs  else ''

class GenerateUrlResponse(GenericResponse):
    """
    Response object Generate URL POST
    """

    def __init__(self,shortUrl="",**kwargs):
        self.shortUrl=shortUrl
        super(GenerateUrlResponse, self).__init__(**kwargs)

class FetchUrlResponse(GenericResponse):
    """
    Fetch URL POST response object
    """
    def __init__(self,longUrl="",**kwargs):
        self.longUrl=longUrl
        super(FetchUrlResponse, self).__init__(**kwargs)

class FetchUrlResponseSerializer(GenericResponseSerializer):
    """
    Fetch Url response serializer
    """
    longUrl=serializers.URLField(required=True)



