#!/usr/bin/env python3

import requests
import unittest
import sys
import random
from hamcrest import *

# Makes HTTP requests bypassing the UI. Requires: python 3, requests and hamcrest libraries.
# To run: from root folder in the terminal, run: "python3 -W ignore -m unittest discover test/"
class QuizzTest(unittest.TestCase):


    def setUp(self):
        self.url = 'http://quizz-app.appspot.com/'


    def test_get_quizz_home_page(self):
        print("\nRunning {}#{}".format(self.__class__.__name__, sys._getframe().f_code.co_name))

        resp = requests.get(self.url)

        assert_that(resp.status_code, is_(equal_to(200)),
                    'Response status code was {}'.format(resp.status_code) )

        assert_that(resp.text, contains_string("The mega quizz - attempt at your own risk!"),
                    "Didn't get the correct HTML for the page.")

        print("Passed")


    def test_aswer_city_question_correctly(self):
        print("\nRunning {}#{}".format(self.__class__.__name__, sys._getframe().f_code.co_name))

        correct_answer = 'Chicago'
        url_param = {'city_query': correct_answer}
        resp = requests.post(self.url+'answer', params=url_param)

        assert_that(resp.status_code, is_(equal_to(200)),
                    'Response status code was {}'.format(resp.status_code) )

        assert_that(resp.text, contains_string("Correct! The answer is %s." % correct_answer),
                    "Failed to verify correct response for city question answered correctly.")
        print("Passed")


    def test_aswer_city_question_incorrectly(self):
        print("\nRunning {}#{}".format(self.__class__.__name__, sys._getframe().f_code.co_name))
        
        # Randomly select from the list of incorrect answers
        incorrect_answer = random.choice(['Indianapolis', 'Del Moines', 'Minneapolis'])
        print("Selected answer: %s." % incorrect_answer)

        url_param = {'city_query': incorrect_answer}
        resp = requests.post(self.url+'answer', params=url_param)

        assert_that(resp.status_code, is_(equal_to(200)),
                    'Response status code was {}'.format(resp.status_code) )


        assert_that(resp.text, contains_string("Incorrect!"),
                    "Failed to verify correct response for city question answered incorrectly.")

        print("Passed")


    def test_aswer_movie_question_correctly(self):
        print("\nRunning {}#{}".format(self.__class__.__name__, sys._getframe().f_code.co_name))

        correct_answer = 'Ghostbusters'
        url_param = {'movie_query': correct_answer}
        resp = requests.post(self.url+'answer', params=url_param)

        assert_that(resp.status_code, is_(equal_to(200)),
                    'Response status code was {}'.format(resp.status_code) )

        assert_that(resp.text, contains_string("Correct! The answer is %s." % correct_answer),
                    "Failed to verify correct response for movie question answered incorrectly.")

        print("Passed")

    def test_aswer_movie_question_incorrectly(self):
        print("\nRunning {}#{}".format(self.__class__.__name__, sys._getframe().f_code.co_name))

        incorrect_answer = random.choice(['Batman', 'Blade', 'Lego Movie'])
        print("Selected answer: %s." % incorrect_answer)

        url_param = {'movie_query': incorrect_answer}
        resp = requests.post(self.url+'answer', params=url_param)

        assert_that(resp.status_code, is_(equal_to(200)),
                    'Response status code was {}'.format(resp.status_code) )


        assert_that(resp.text, contains_string("Incorrect!"),
                    "Failed to verify correct response for movie question answered incorrectly.")

        print("Passed")


    def test_aswer_car_question_correctly(self):
        print("\nRunning {}#{}".format(self.__class__.__name__, sys._getframe().f_code.co_name))

        correct_answer = 'Delorean'
        url_param = {'car_query': correct_answer}
        resp = requests.post(self.url+'answer', params=url_param)

        assert_that(resp.status_code, is_(equal_to(200)),
                    'Response status code was {}'.format(resp.status_code) )

        assert_that(resp.text, contains_string("Correct! The answer is %s." % correct_answer),
                    "Failed to verify correct response for car question answered incorrectly.")

        print("Passed")


    def test_aswer_car_question_incorrectly(self):
        print("\nRunning {}#{}".format(self.__class__.__name__, sys._getframe().f_code.co_name))

        incorrect_answers = ['Ferrari', 'Corvette', 'Porsche']
        select_answer = (random.choice(incorrect_answers))

        print("Selected answer: %s." % select_answer)
        incorrect_answer = 'Ferrari'
        url_param = {'car_query': select_answer}
        resp = requests.post(self.url+'answer', params=url_param)

        assert_that(resp.status_code, is_(equal_to(200)),
                    'Response status code was {}'.format(resp.status_code) )


        assert_that(resp.text, contains_string("Incorrect!"),
                    "Failed to verify correct response for car question answered incorrectly.")

        print("Passed")


    def test_user_is_unable_to_answer_a_question_multiple_times(self):
        print("\nRunning {}#{}".format(self.__class__.__name__, sys._getframe().f_code.co_name))

        s = requests.Session()

        correct_answer = 'Ghostbusters'
        url_param = {'movie_query': correct_answer}
        resp = s.post(self.url+'answer', params=url_param)

        got_cookie = resp.cookies

        assert_that(str(got_cookie), contains_string("Cookie movie_guesses=1|226f50383724908ce222af203765afad for quizz-app.appspot.com"))

        assert_that(resp.text, contains_string("Correct! The answer is %s." % correct_answer),
                    "Failed to verify correct response for city question answered correctly.")


        #  Now make a second request simulating a user attempting the answer the question again
        second_resp = s.post(self.url+'answer', params=url_param)

        got_cookie = second_resp.cookies

        # Amount of guesses cookie should be now set to 2. User should get appropriate response.
        assert_that(str(got_cookie), contains_string("Cookie movie_guesses=2|45f107ae152fb420cab04e9a00b73a09 for quizz-app.appspot.com"))

        assert_that(second_resp.text, contains_string("You've already attempted this question."),
                    "Failed to verify that user is prevented from answering the questions multiple times!")

        print("Passed")