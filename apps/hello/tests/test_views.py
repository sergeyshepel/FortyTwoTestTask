# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse

from hello.models import Person

NUMBER_OF_PERSON = 10


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


class IndexViewTests(TestCase):
    """
    Test index view on rendering correct data
    """

    def test_index_view_to_be_resolved_by_root_url(self):
        """
        Check if index view could be resolved by root url
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_index_view_return_correct_template(self):
        """
        Index function should return correct template
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hello/index.html')

    def test_index_view_return_empty_reply(self):
        """
        Index function should return message when no data in db
        """
        Person.objects.all().delete()
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No records found in db!")
        self.assertEqual(response.context['person'], None)

    def test_index_view_return_correct_value(self):
        """
        Index function should return correct item from database
        """
        person = Person.objects.first()
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        # Check if encoding is correct
        self.assertContains(response, 'utf-8')
        self.assertContains(response, person.first_name)
        self.assertContains(response, person.last_name)
        self.assertContains(response, person.email)

    def test_index_view_if_more_than_one_person_id_db(self):
        """
        Test render of index page when more than one person in db
        """
        for i in range(0, NUMBER_OF_PERSON):
            Person.objects.create(first_name="Vasilii" + str(i),
                                  last_name="Pupkin" + str(i),
                                  date_of_birthday="2014-02-01",
                                  bio="Not very tall" + str(i),
                                  email="testemail@email.com",
                                  jabber="" + str(i),
                                  skype="echo123" + str(i),
                                  other_contacts="No other contacts" + str(i))
        people = Person.objects.all().count()
        self.assertEqual(people, 11)
        person = Person.objects.first()
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        # Check if encoding is correct
        self.assertContains(response, 'utf-8')
        self.assertEqual(response.context['person'], person)
        self.assertContains(response, person.first_name)
        self.assertContains(response, person.last_name)
        self.assertContains(response, person.email)
        self.assertNotContains(response, 'Vasilii0')
        self.assertNotContains(response, 'Pupkin0')
        self.assertNotContains(response, 'testemail@email.com')
