# -*- coding: utf-8 -*-
import json

from django.test import TestCase

from django.core.urlresolvers import reverse

from hello.models import Person, Requests
from hello.forms import PersonForm

NUMBER_OF_PERSON = 10


class IndexViewTests(TestCase):
    """
    Test index view on rendering correct data
    """

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
    """
    Test requests view on rendering correct data
    """

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

    def test_requests_page_shows_sorted_via_priority_records(self):
        """ Check if requests with the highest priority go first """

        for i in range(5):
            self.client.get(reverse('index'))

        response = self.client.get(reverse('requests'))

        rendered_priority_list = []
        for item in response.context['new_requests']:
            rendered_priority_list.append(item.priority)

        requests_sorted_via_priority = []
        ten_requests = Requests.objects.all()[:10]
        requests = sorted(ten_requests, key=lambda x: x.priority, reverse=True)
        for request in requests:
            requests_sorted_via_priority.append(request.priority)

        self.assertEquals(rendered_priority_list, requests_sorted_via_priority)


class EditViewTests(TestCase):
    """
    Test edit view on rendering correct data and proper functionality
    """

    def test_could_be_resolved(self):
        """ Check if edit view could be resolved """
        login = self.client.login(username='admin', password='admin')
        self.assertTrue(login)
        response = self.client.get(reverse('edit', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_return_correct_template(self):
        """ Edit view should render correct template """
        login = self.client.login(username='admin', password='admin')
        self.assertTrue(login)
        response = self.client.get(reverse('edit', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hello/edit.html')

    def test_edit_page_could_not_be_accessed_without_auth(self):
        """
        Anonymous user could not get edit page and
        should be redirected on login page
        """
        response = self.client.get(reverse('edit', args=[1]))
        self.assertRedirects(response, "%s?next=%s" % (
            reverse('login'), reverse('edit', args=[1])), 302, 200)

    def test_edit_view_returns_instantiated_person_form(self):
        """ Edit view should return person_form with specific instance """
        login = self.client.login(username='admin', password='admin')
        self.assertTrue(login)
        response = self.client.get(reverse('edit', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['person_form'], PersonForm)

    def test_edit_page_renders_person_form(self):
        """ Edit page renders person_form """
        login = self.client.login(username='admin', password='admin')
        self.assertTrue(login)
        person = Person.objects.first()
        person_object_fields = person._meta.fields
        response = self.client.get(reverse('edit', args=[1]))
        self.assertContains(response, 'utf-8')
        for field in person_object_fields:
            if field.name != 'id':
                self.assertIn('id_' + str(field.name), response.content)
            else:
                pass
        self.assertIn('commonform', response.content)

    def test_edit_view_updates_Person_model_via_ajax(self):
        """
        Ajax post method for commonform
        Form should update Person object
        """
        login = self.client.login(username='admin', password='admin')
        self.assertTrue(login)
        person = Person.objects.first().__dict__
        person['first_name'] = u'Puzik'
        response = self.client.post(reverse('edit', args=[1]),
                                    person,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        updated_person = Person.objects.first()
        self.assertEquals(updated_person.first_name, person['first_name'])
        self.assertEquals(json.loads(response.content)['msg'],
                          'Record was updated successfully')

    def test_edit_view_does_not_updates_Person_model_without_ajax(self):
        """ Post method for commonform form should not update Person object """
        login = self.client.login(username='admin', password='admin')
        self.assertTrue(login)
        person = Person.objects.first().__dict__
        person['first_name'] = u'Puzik'
        self.client.post(reverse('edit', args=[1]), person)
        updated_person = Person.objects.first()
        self.assertNotEquals(updated_person.first_name, person['first_name'])

    def test_edit_view_does_not_updates_Person_model_with_invalid_data(self):
        """
        Ajax post method with invalid data,
        should not update Person object
        """
        login = self.client.login(username='admin', password='admin')
        self.assertTrue(login)
        person = Person.objects.first().__dict__
        person['first_name'] = u''
        response = self.client.post(reverse('edit', args=[1]),
                                    person,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(
            json.loads(response.content)['first_name'][0],
            u'This field is required.'
        )


class TemplateTagTests(TestCase):
    """
    Check edit_link tag render
    """
    def test_edit_link_tag_render(self):
        """ Check if edit_link rendered on index page """
        login = self.client.login(username='admin', password='admin')
        self.assertTrue(login)
        response = self.client.get(reverse('index'))
        person_pk = response.context['person'].pk
        admin_url = reverse("admin:%s_%s_change" %
                            (Person._meta.app_label, Person._meta.model_name),
                            args=[person_pk])
        self.assertIn('<a href="' + admin_url + '">(admin)</a>',
                      response.content)
