The app runs on Google App Engine. URL: http://quizz-app.appspot.com/

Noteable things: to prevent user cheating the quiz by answering a question multiple times, I implementing setting a cookie
that tracks number of attempts for every question. The cookie is hashed using HMAC: https://docs.python.org/2/library/hmac.html
and "salted" with a secret string.


To run tests you need:

* Python 3: https://www.python.org/downloads/
* requests library: http://docs.python-requests.org/en/latest/user/install/#install
* hamcrest matchers  library: https://pypi.python.org/pypi/PyHamcrest
	- run "sudo pip install pyhamcrest"