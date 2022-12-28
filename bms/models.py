from django.db import models
from django.db.models.base import Model
from django.db.models.query import QuerySet
#from accounts.models import Departments
from django.core.exceptions import FieldError
import datetime
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.forms import DateTimeInput
from django.contrib.admin.widgets import AdminDateWidget,AdminTimeWidget, AdminSplitDateTime
from django.template.defaultfilters import filesizeformat
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import InlineRadios
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div
# Create your models here.
##for sentinal user deleted user data
def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

def book_cover_dir(instance, filename):
    return f'uploads/{instance.owner.id}/book-covers/{filename}'

def book_dir(instance, filename):
    return f'uploads/{instance.owner.id}/books/{filename}'


class CustomAdminSplitDateTime(AdminSplitDateTime):
    def __init__(self, attrs=None):
        widgets = [AdminDateWidget, AdminTimeWidget(attrs=None, format='%I:%M %p')]
        forms.MultiWidget.__init__(self, widgets, attrs)

class Book(models.Model):
    title=models.CharField(max_length=200, null=True, blank=True)
    book_file = models.FileField(upload_to=book_dir, null=True, blank=True)
    author=models.CharField(max_length=200, null=True, blank=True)
    title_image=models.ImageField(upload_to =book_cover_dir,null=True, blank=True)
    language=models.CharField(max_length=100, null=True, blank=True)
    datetime_update=models.DateTimeField(default=datetime.datetime.now)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET(get_sentinel_user), default=None,to_field='username', null=True, blank=True)
    identifier=models.CharField(max_length=200, null=True, blank=True)
    date_of_book=models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return f"Owner: {self.owner} | {self.title}"