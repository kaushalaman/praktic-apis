import scipy.io.wavfile as wavfile
import os

def readAudioFile(path):
    extension = os.path.splitext(path)[1]
    try:
        if extension.lower() == '.wav':
            [Fs, x] = wavfile.read(path)
        elif extension.lower() == '.aif' or extension.lower() == '.aiff':
            s = aifc.open(path, 'r')
            nframes = s.getnframes()
            strsig = s.readframes(nframes)
            x = numpy.fromstring(strsig, numpy.short).byteswap()
            Fs = s.getframerate()
        else:
            print("Error in readAudioFile(): Unknown file type!")
            return (-1,-1)
    except IOError:
        print("Error: file not found or other I/O error.")
        return (-1,-1)
    return (Fs, x)


def handleUploadedFile(f):
    base_filename           = 'temp';
    suffix                  = '.wav'
    BASE_DIR                = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MEDIA_DIR               = os.path.join(BASE_DIR, "media")
    INCOMING_VOICE_DIR      = os.path.join(MEDIA_DIR, "incomingVoice")
    filePath                = os.path.join(INCOMING_VOICE_DIR, base_filename + suffix)
    with open(filePath, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    return filePath
