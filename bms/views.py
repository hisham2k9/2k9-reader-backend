from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,FileResponse
from bms.serializers import BookSerializer, GenericResponse, GenericResponseSerializer
from django.core.serializers.json import DjangoJSONEncoder
from bms.services import get_epub_cover,epub_info
from .models import Book
from zipfile import ZipFile
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication,permissions
import pytz,uuid,io,logging,traceback,datetime,json
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.response import Response
from django.core.files.images import ImageFile
from django.core import serializers
from django.conf import settings
from utils.custom_log_writer import log


    
    
    

class BooksView(APIView):
    """
    view on CRUD on books
    """
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        """
        returns book list or particular book if id is !=0
        """
        _id = str(uuid.uuid4())
        try:
            log(request, _id, request.path, "",None )
            context={}
            qs= Book.objects.filter(owner=request.user).filter(is_active=True)
            data = serializers.serialize("json", qs)
            context["data"]=json.loads(data)
            responseObject=GenericResponse(_id,details=[context])
            response=GenericResponseSerializer(responseObject)
            log(request, _id, request.path, response.data,None )
            return Response(response.data, status = 200)
        except:
            traceback.print_exc()
            responseObject=GenericResponse(_id,status="-1",errorMessage=["unknown error"])
            response=GenericResponseSerializer(responseObject)
            log(request, _id, request.path, response.data,traceback.format_exc() )
            return Response(response.data, status = 500)
        
        

class BookView(APIView):
    """
    View for CRUD on Book
    """
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = (IsAuthenticated,)
    
    def delete(self,request,pk=0):
        """
        delete book
        """
        
        _id = str(uuid.uuid4())
        try:
            log(request, _id, request.path, "",None )
            response=GenericResponse(_id,data={},partial=True)
            book = Book.objects.filter(owner=request.user).filter(id=pk).filter(is_active=True)
            if request.path != f"/book/{str(pk)}":
                raise Exception ("User Media Download Unavailable")
            if book:
                book[0].is_active=False
                book[0].save()
                responseObject=GenericResponse(_id,details=["Book Deleted"])
                response=GenericResponseSerializer(responseObject)
                log(request, _id, request.path, response.data,None )
                return Response(response.data, status = 200)
            else:
                raise ValueError("Book/Owner combo not found")
            
        except ValueError as ex:
            responseObject=GenericResponse(_id,status="-1",errorMessage=[str(ex)])
            response=GenericResponseSerializer(responseObject)
            log(request, _id, request.path, response.data,traceback.format_exc())
            return Response(response.data, status = 401)

        except Exception as ex:
            traceback.print_exc()
            responseObject=GenericResponse(_id,status="-1",errorMessage=[str(ex)])
            response=GenericResponseSerializer(responseObject)
            log(request, _id, request.path, response.data,traceback.format_exc())
            return Response(response.data, status = 500)

    def get(self, request,pk=0):
        """
        returns single book as file response
        """
        _id = str(uuid.uuid4())
        try:
            log(request, _id, request.path, "",None )
            response=GenericResponse(_id,data={},partial=True)
            book = Book.objects.filter(owner=request.user).filter(id=pk).filter(is_active=True)
            if request.path != f"/book/{str(pk)}":
                raise Exception ("User Media Download Unavailable")
            if book:
                book_file = book[0].book_file.name
                log(request, _id, request.path, response.data,None )
                return FileResponse(open(settings.MEDIA_ROOT+'/'+book_file, 'rb'))
            else:
                raise ValueError("Book/Owner combo not found")
        except ValueError as ex:
            responseObject=GenericResponse(_id,status="-1",errorMessage=[str(ex)])
            response=GenericResponseSerializer(responseObject)
            log(request, _id, request.path, response.data,traceback.format_exc())
            return Response(response.data, status = 401)

        except Exception as ex:
            traceback.print_exc()
            responseObject=GenericResponse(_id,status="-1",errorMessage=[str(ex)])
            response=GenericResponseSerializer(responseObject)
            log(request, _id, request.path, response.data,traceback.format_exc())
            return Response(response.data, status = 500)

    def post(self, request):
        """
        Saves new book upload
        """
        _id = str(uuid.uuid4())
        try:
            log(request, _id, request.body[:1000], "",None )
            response=GenericResponse(_id,data={},partial=True)
            book_data = BookSerializer(data=request.data)
            if book_data.is_valid():
                book =  Book()
                book.book_file = book_data.validated_data["book_file"]
                book_zip = request.FILES["book_file"]
                title_image = ImageFile(io.BytesIO(get_epub_cover(book_zip)), f"{book.book_file.name}.png")  # << the answer!
                book.title_image = title_image
                book.is_active = True
                book.owner = request.user
                book.datetime_update = datetime.datetime.now(tz=pytz.UTC)
                book_meta = epub_info(book_zip)
                book.title=book_meta["title"]
                book.language=book_meta["language"]
                book.author=book_meta["creator"]
                book.date_of_book = book_meta["date"]
                book.identifier = book_meta["identifier"]
                book.save()
                responseObject=GenericResponse(_id,details=[book_meta])
                response=GenericResponseSerializer(responseObject)
                log(request, _id, request.body[:1000], response.data,None )
                return Response(response.data, status = 200)
            else:
                raise ValueError(str(book_data.errors))
        except ValueError as ex:
            traceback.print_exc()
            responseObject=GenericResponse(_id,status="-2",errorMessage=[str(ex)])
            response=GenericResponseSerializer(responseObject)
            log(request, _id, request.body[:1000], response.data,traceback.format_exc())
            return Response(response.data, status = 400)
        except Exception as ex:
            traceback.print_exc()
            responseObject=GenericResponse(_id,status="-1",errorMessage=[str(ex)])
            response=GenericResponseSerializer(responseObject)
            log(request, _id, request.body[:1000], response.data,traceback.format_exc())
            return Response(response.data, status = 500)

