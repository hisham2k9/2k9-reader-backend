from django.forms import ModelForm,forms
from .models import Book
from django.core.exceptions import ValidationError


#file upload validation, action completion 
# def check_is_epub(value): # add this to some file where you can import it from
#     if not value.file.name.tolower().endswith(".epub"):
#         raise ValidationError('File may not be desired format. Unable to process!')

# class BookForm(ModelForm):
#     book_file=forms.FileField(label='Book File', required=True,widget=forms.ClearableFileInput(attrs={'id':'file'}),validators=[file_size])
#     class Meta:
#         model=Book
#         fields=['book_file']  