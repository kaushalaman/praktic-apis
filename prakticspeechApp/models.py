from __future__ import unicode_literals
from django.db import models

# Create your models here.
class AudioFile(models.Model):
    options = (('1', 'speaker_recognition'), ('2', 'language_detection'))
    type_of_system  = models.CharField(max_length = 1, choices = options)
    username        = models.CharField(max_length = 255, unique = True)
    audioFile       = models.FileField(upload_to='uploads/')
    uploaded_at     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.type_of_system
