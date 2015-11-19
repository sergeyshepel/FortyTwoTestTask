# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse

from hello.models import Person, Requests

NUMBER_OF_PERSON = 10


class IndexViewTests(TestCase):
    """ Test index view on rendering correct data """

    def test_index_view_to_be_resolved_by_root_url(self):
        """ Check if index view could be resolved by root url """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_index_view_return_correct_template(self):
        """ Index function should return correct template """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hello/index.html')

    def test_index_view_return_empty_reply(self):
        """ Index function should return message when no data in db """
        Person.objects.all().delete()
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No records found in db!")
        self.assertEqual(response.context['person'], None)

    def test_index_view_return_correct_value(self):
        """ Index function should return correct item from database """
        person = Person.objects.first()
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        # Check if encoding is correct
        self.assertContains(response, 'utf-8')
        self.assertContains(response, person.first_name)
        self.assertContains(response, person.last_name)
        self.assertContains(response, person.email)

    def test_index_view_if_more_than_one_person_id_db(self):
        """ Test render of index page when more than one person in db """
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


class RequestsViewTests(TestCase):
    """ Test requests view on rendering correct data """

    def test_could_be_resolved(self):
        """ Check if requests view could be resolved """
        response = self.client.get(reverse('requests'))
        self.assertEqual(response.status_code, 200)

    def test_return_correct_template(self):
        """ Requests function should returns correct template """
        response = self.client.get(reverse('requests'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hello/requests.html')

    def test_requests_page_return_correct_number_of_records(self):
        """ Requests function should returns 10 records from db """
        for i in range(0, 20):
            response = self.client.get(reverse('requests'))
            self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['new_requests']), 10)

    def test_if_requests_view_returns_valid_data(self):
        """ Check if Requests function returns valid data """
        response = self.client.get(reverse('requests'))
        self.assertEqual(response.status_code, 200)
        content = response.context['new_requests'][0]
        data = Requests.objects.first()
        self.assertEqual(content, data)

    def test_middleware_doesnt_save_ajax_requests(self):
        """ Check if middleware doesn't save ajax requests on requests page"""
        self.client.get(reverse('requests'),
                        HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        requsts_stored_in_db = Requests.objects.all().count()

        self.assertEquals(requsts_stored_in_db, 0)
