from rest_framework import serializers
from .models import Book
from rest_framework import serializers
import datetime
import pytz
from django.conf import settings
from zoneinfo import ZoneInfo


class BookSerializer(serializers.ModelSerializer):
    book_file = serializers.FileField(label="bookFile")
    def validate(self, data):
        if  not data['book_file'].name.lower().endswith(".epub"):
            raise serializers.ValidationError("File is not epub")
        return data

    class Meta:
        model = Book
        fields=["book_file"]



class GenericResponseSerializer(serializers.Serializer):
    """
    Default response serializer
    """
    transactionId=serializers.CharField(max_length=50)
    status=serializers.CharField(max_length=5)
    errorMessage=serializers.ListField()
    details=serializers.ListField()
    


class GenericResponse(object):
    """
    Default response object
    """
    def __init__(self,_id,**kwargs):
        self.transactionId=_id
        self.status=kwargs['status'] if 'status' in kwargs else '0'
        self.errorMessage=kwargs['errorMessage'] if 'errorMessage' in kwargs else []
        self.details=kwargs['details'] if 'details' in kwargs else []
        

