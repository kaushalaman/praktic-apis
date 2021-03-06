from __future__ import unicode_literals
from django.db import models

# Create your models here.

def get_upload_to(instance, filename):
    return 'uploads/%s/%s' % (instance.username, filename)


class AudioFile(models.Model):
    options = (('1', 'speaker_recognition'), ('2', 'language_detection'))
    type_of_system          = models.CharField(max_length = 1, choices = options)
    username                = models.CharField(max_length = 255, unique = True)
    audioFile               = models.FileField(upload_to=get_upload_to)
    hashData                = models.CharField(max_length = 255)
    signalFFTData           = models.CharField(max_length = 255)
    numberOfRows            = models.IntegerField(default = 0)
    numberOfColumns         = models.IntegerField(default = 0)
    signalFFTDataNPString   = models.TextField(max_length = 255)
    numpyDataType           = models.CharField(max_length = 255, default='float')
    uploaded_at             = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.type_of_system+" "+ self.username
