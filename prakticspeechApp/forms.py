from django import forms
from prakticspeechApp.models import AudioFile

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = AudioFile
        fields = ('type_of_system', 'username', 'audioFile')
