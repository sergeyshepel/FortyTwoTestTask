# -*- coding: utf-8 -*-
import datetime

from django.test import TestCase
from hello.models import Person, Requests


class PersonModelTest(TestCase):
    """
    Test the creation of new object in Person table
    """

    def create_person(self):
        return Person.objects.create(first_name="Vasilii",
                                     last_name="Pupkin",
                                     date_of_birthday="2014-02-01",
                                     bio="Not very tall",
                                     email="testemail@email.com",
                                     jabber="",
                                     skype="echo123",
                                     other_contacts="No other contacts")

    def test_person_creation(self):
        """
        Test if new object was created
        """
        person = self.create_person()
        person_unicode = (person.first_name + " " +
                          person.last_name + " " +
                          person.email)
        self.assertTrue(isinstance(person, Person))
        self.assertEqual(person.__unicode__(), person_unicode)


class RequestsModelTest(TestCase):
    """
    Test the creation of new object in Requests table
    """

    def create_request(self):
        """
        Create new object
        """
        return Requests.objects.create(time=datetime.datetime.now(),
                                       path="/",
                                       method="GET",
                                       user_agent="Mozilla/5.0",
                                       remote_addr="127.0.0.1",
                                       is_secure="False",
                                       is_ajax="False")

    def test_request_creation(self):
        """
        Test if new object created
        """
        request = self.create_request()
        request_unicode = (str(request.time) + " " +
                           str(request.path) + " " +
                           str(request.remote_addr))
        self.assertTrue(isinstance(request, Requests))
        self.assertEqual(request.__unicode__(), request_unicode)
