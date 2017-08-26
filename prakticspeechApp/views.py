from django.shortcuts import render
from django.http import HttpResponse
from prakticspeechApp.models import AudioFile
from prakticspeechApp.forms import UploadFileForm
from django.conf import settings
# Create your views here.

def index(request):
    return render(request, 'prakticspeechApp/index.html')

def handle_uploaded_file(fileData):
    print("fileData",fileData)

def storeFileData(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = UploadFileForm()
    return render(request, 'prakticspeechApp/form.html', {'form': form})
