#!/usr/bin/env python

import webapp2
import jinja2
import cgi
import os
import urllib
import hmac
from google.appengine.ext import db
from google.appengine.ext.webapp import template


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class City(db.Model):
    name = db.StringProperty(required = True)

class Movie(db.Model):
    name = db.StringProperty(required = True)

class Car(db.Model):
    name = db.StringProperty(required = True)

class MainHandler(webapp2.RequestHandler):

    def get(self):
        cities = db.GqlQuery('SELECT DISTINCT name FROM City')
        movies = db.GqlQuery('SELECT DISTINCT name FROM Movie')
        cars = db.GqlQuery('SELECT DISTINCT name FROM Car')

    	values = {
            'cities': cities,
            'movies': movies,
            'cars': cars
    	}
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(template.render('main.html', values))

        # MainHandler.populateDatabase(self)

    # # Used to pre-populate the db with data
    # def populateDatabase(self):
    #     cities = [City(name="Chicago"), City(name='Indianpolis'), City(name='Minneapolis'), City(name='Des Moines')]
    #     for city in cities:
    #         city.put()

    #     movies = [Movie(name="Batman"), Movie(name='Lego Movie'), Movie(name='Blade'), Movie(name='Ghostbusters')]
    #     for movie in movies:
    #         movie.put()

    #     cars = [Car(name="Corvette"), Car(name='Ferrari'), Car(name='Delorean'), Car(name='Porsche')]
    #     for car in cars:
    #         car.put()


# Handles the POST request to /answer
class AnswerHandler(webapp2.RequestHandler):

    def post(self):
        answer = self.request.arguments()[0]

        if answer == "city_query":
            city_guesses_cookie_str = AnswerHandler.setNumOfAttemptsCookie(self, 'city_guesses')
            AnswerHandler.checkNumCoookiesAndDisplayAnswer(self,
                                                           'city_query', 
                                                           city_guesses_cookie_str, 
                                                           'Chicago')

        elif answer == "movie_query":
            movie_guesses_cookie_str = AnswerHandler.setNumOfAttemptsCookie(self, 'movie_guesses')
            AnswerHandler.checkNumCoookiesAndDisplayAnswer(self, 
                                                           'movie_query', 
                                                           movie_guesses_cookie_str, 
                                                           'Ghostbusters')

        elif answer == "car_query":    
            car_guesses_cookie_str = AnswerHandler.setNumOfAttemptsCookie(self, 'car_guesses')
            AnswerHandler.checkNumCoookiesAndDisplayAnswer(self, 
                                                           'car_query', 
                                                           car_guesses_cookie_str, 
                                                           'Delorean')

        self.response.out.write(template.render('templates/back-button.html', None))


    # Set a cookie for a number of attempts to answer the question
    # i.e. set-cookie:car_guesses=5|da319be47f08b1714211f8f315493e86
    @staticmethod
    def setNumOfAttemptsCookie(self, cookie):

        guesses = 0     
        guesses_cookie_str = self.request.cookies.get(cookie)

        sec = Secured()
        if guesses_cookie_str:
            cookie_val = sec.check_secure_val(guesses_cookie_str)
            if cookie_val:
                guesses = int(cookie_val)

        guesses += 1

        new_cookie_val = sec.make_secure_val(str(guesses))

        self.response.headers.add_header('Set-Cookie', '{cookie}={value}'.format(cookie=cookie, value=new_cookie_val))

        return guesses_cookie_str

    # Check number of attempts, display the feedback or tell them there are no more tries
    @staticmethod
    def checkNumCoookiesAndDisplayAnswer(self, url_param, num_of_attempts, corr_answer):
        if num_of_attempts <= 1:
            # Convert the characters '&', '<' and '>' to HTML-safe sequences.
            answer = cgi.escape(self.request.get(url_param))

            if str(answer) == corr_answer:
                self.response.out.write("Correct! The answer is %s." % str(corr_answer))
            else: 
                self.response.out.write("Incorrect!")
        else:
            self.response.write("You've already attempted this question.")


# Used to encrypt and salt the cookie so it could not be forged thus letting the 
# test-taker reset the number of attempts
class Secured():
    # To "salt" the cookie
    SECRET = 'mylittlesecret'

    def hash_str(self, s):
        return hmac.new(Secured.SECRET, s).hexdigest()

    # Return cookie value and hashed value
    # i.e. 5|da319be47f08b1714211f8f315493e86
    def make_secure_val(self, s):
        return "%s|%s" % (s, self.hash_str(s))

    # Check that the hash of the cookie matches expected
    def check_secure_val(self, h):
        val = h.split("|")[0]
        if h == self.make_secure_val(val):
            return val

app = webapp2.WSGIApplication([('/', MainHandler), ('/answer', AnswerHandler)],debug=True)
