from django.shortcuts import render
from django.http import HttpResponse
from prakticspeechApp.models import AudioFile
from prakticspeechApp.forms import UploadFileForm, loginVoiceForm
from django.conf import settings
import time
import os
from prakticspeechApp.utility import readAudioFile, handleUploadedFile
from scipy.fftpack import fft, ifft
import numpy as np
import hashlib
import json
from bson import json_util
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def index(request):
    return render(request, 'prakticspeechApp/index.html')

@csrf_exempt
def registerUserVoice(request):
    retError = dict()
    ret = dict()
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                if request.POST['type_of_system'] is not "1":
                    retError["message"] = 'Type Of system should be `speaker_recognition` (1).'
                    retError["status_code"] = 400
                    retError["success"] = False
                    retError["data"] = []
                    return HttpResponse(json.dumps(retError), content_type="application/json")
                form.save()
                """
                Generate Delay of 1 Second
                """
                time.sleep(1)
                audioData = AudioFile.objects.filter(username=request.POST['username']).values()
                BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                audioFilePathOfUser =  BASE_DIR +settings.MEDIA_URL + audioData[0]['audioFile']
                t = readAudioFile(audioFilePathOfUser)
                """
                    Zero padded Numpy array before taking FFT and create FFT signal numpy array
                """
                FFTData = fft(np.pad(np.array(t[1]),(0, len(t[1])), 'constant'))
                sizeFFTData = np.array(FFTData).shape
                numberOfRows = sizeFFTData[0]
                if len(sizeFFTData)>1:
                    numberOfColumns = sizeFFTData[1]
                numberOfColumns = 0
                numpyDataType = np.array(FFTData).dtype
                signalFFTData = np.array_str(np.array(FFTData))
                """
                 store hash data of FFT signal
                """
                hashData = hashlib.sha1(np.array(FFTData)).hexdigest()
                AudioFile.objects.filter(username=request.POST['username']).update(signalFFTData=signalFFTData, hashData = hashData
                ,numpyDataType = numpyDataType,numberOfRows = numberOfRows, numberOfColumns = numberOfColumns)
                audioData = AudioFile.objects.filter(username=request.POST['username']).values()
                """
                    Return Success JSON
                """
                ret["message"] = 'User registered by voice and Training successful'
                ret["status_code"] = 200
                ret["success"] = True
                ret["data"] = list(audioData)
                return HttpResponse(json.dumps(ret, default=json_util.default), content_type="application/json")
            except Exception as e:
                retError["message"] = 'Error in user registration or Training'
                retError["status_code"] = 400
                retError["success"] = False
                retError["data"] = []
                return HttpResponse(json.dumps(retError), content_type="application/json")
        else:
            retError["message"] = 'User is already registered.'
            retError["status_code"] = 400
            retError["success"] = False
            retError["data"] = []
            return HttpResponse(json.dumps(retError), content_type="application/json")
    else:
        form = UploadFileForm()
        return render(request, 'prakticspeechApp/form.html', {'form': form})

@csrf_exempt
def loginUserByVoice(request):
    retError = dict()
    ret = dict()
    if request.method == 'POST':
        form = loginVoiceForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                audioData = AudioFile.objects.filter(username=username).values()
                if audioData and len(audioData):
                    foundUserHashData = audioData[0]['hashData']
                    foundUserDtype = audioData[0]['numpyDataType']
                    tempFoundUserVoiceFFTData = audioData[0]['signalFFTData'][1:len(audioData[0]['signalFFTData'])-1]
                    try:
                        foundUserVoiceFFTData = np.fromstring(tempFoundUserVoiceFFTData, dtype=foundUserDtype, sep=' ')
                    except:
                        print("Not able read numpy data")
                    incomingFile = request.FILES['audioFile']
                    try:
                        filePath = handleUploadedFile(incomingFile)
                    except:
                        retError["message"] = 'File Write On Disk Error'
                        retError["status_code"] = 400
                        retError["success"] = False
                        retError["data"] = []
                        return HttpResponse(json.dumps(retError), content_type="application/json")

                    t = readAudioFile(filePath)
                    """
                        Zero padded Numpy array before taking FFT and create FFT signal numpy array
                    """
                    incomingFFTData = fft(np.pad(np.array(t[1]),(0, len(t[1])), 'constant'))
                    incomingHashData = hashlib.sha1(np.array(incomingFFTData)).hexdigest()
                    incomingSignalFFTData = np.array(incomingFFTData)
                    incomingSignalFFTData = np.array_str(np.array(incomingSignalFFTData))
                    if incomingSignalFFTData == audioData[0]['signalFFTData'] or incomingHashData == foundUserHashData:
                        ret["message"] = 'login successfully'
                        ret["status_code"] = 200
                        ret["success"] = True
                        ret["data"] = []
                        return HttpResponse(json.dumps(ret), content_type="application/json")
                    else:
                        retError["message"] = 'You cannot login'
                        retError["status_code"] = 400
                        retError["success"] = False
                        retError["data"] = []
                        return HttpResponse(json.dumps(retError), content_type="application/json")
                else:
                    retError["message"] = 'User is not registered'
                    retError["status_code"] = 400
                    retError["success"] = False
                    retError["data"] = []
                    return HttpResponse(json.dumps(retError), content_type="application/json")
            except Exception as e:
                retError["message"] = 'Error in user login'
                retError["status_code"] = 400
                retError["success"] = False
                retError["data"] = []
                return HttpResponse(json.dumps(retError), content_type="application/json")
        else:
            retError["message"] = 'Invalid Data in form.'
            retError["status_code"] = 400
            retError["success"] = False
            retError["data"] = []
            return HttpResponse(json.dumps(retError), content_type="application/json")
    else:
        form = loginVoiceForm()
        return render(request, 'prakticspeechApp/form.html', {'form': form})
