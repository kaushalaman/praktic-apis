Voice Authentication System:


###URLS:

1. GET API: http://127.0.0.1:8000/voice/registerUserVoice/ will give you HTML form for register user voice.

2. POST API: http://127.0.0.1:8000/voice/registerUserVoice/ will register user and train voice data

FormData: {
  type_of_system: '1' (or '2')
  username: 'aman'
  audioFile: FILE
}

3. GET API: http://127.0.0.1:8000/voice/loginUserByVoice/ will give you HTML Form for login user through voice

4. POST API: http://127.0.0.1:8000/voice/loginUserByVoice/ will authenticate user

FormData: {
  username: 'aman',
  audioFile: FILE
}


###DATABASE: mysql

###TEMPLATES: FORMS and INDEX Html FILES

###PYTHON LIBRARIES: NUMPY, SCIPY, BSON

###Algorithm:

1. Retrieve Fast Fourier Transform of Input signal with zeros padding in end and create a SHA Hash for Input Signal (Done)
2. Retrieve Fast Fourier Transform of Stored User Voice signal with zeros padding in end and create SHG Hash (Done)
3. Match both FFTs if they are nearly equal .. login successful or  check Both SHAs are equal if they are ...login successful (Done)
4. Otherwise Check auto correlation of both signals FFTs if auto correlation is high .. close to 1 ....login successful (Pending .. Time constraint)

5. If no match is found then ...login unsuccessful

###Models:
Database Model `AudioFile` is defined in models.py in prakticspeechApp directory

###Note (Things Pending due to time limitation):

---I have used Mysql, but since data was unstructured therefore i should have used NoSql or PostGreSQL for SQl. But i could not change
Database server.
--- I stored nupmy array in mysql in string format which when retrieved. numpy is not able to read it. I could not troubleshoot it for now.
--- autocorrelation thing left pending
--- deployment at herokuapp
--- Application can be made better with more digital signal processing mechanisms and
signal features/patterns matching algorithms. (Need to fetch MFCC, LPC, Enrgy features)


How to Run:

1. Install Django, anaconda packages
2. Go To Application directory
3. Create Mysql Database `praktic`
4. Run: `python manage.py migrate`
5. Run: `python manage.py makemigrations prakticspeechApp`
6. Run: `python manage.py migrate` (Again)
7. Run: `python manage.py runserver`
8. Use Get APIS (Forms) to Hit POST request or use POSTMAN
9. IF you use POSTMAN then Please provide 'CSRF token' from cookie for that you can
install 'interceptor' plugin which once enabled, can provide you csrf token from cookie data
Note: The CSRF middleware and template tag provides easy-to-use protection against Cross Site Request Forgeries. for
Security purpose I used it.


Submitted By:
Aman Kaushal
https://www.linkedin.com/in/amankaushaliiitm/
