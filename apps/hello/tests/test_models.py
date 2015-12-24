# -*- coding: utf-8 -*-
import datetime

from django.test import TestCase
from hello.models import Person, Requests, DBActionsLog, Team

from apps.hello import signals  # NOQA

NUMBER_OF_MEMBERS = 10
NUMBER_OF_TEAMS = 10


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


class DBActionsLogModelTest(TestCase):
    """
    Test loggining of db actions with signals
    """

    def test_object_created_action(self):
        """ Check if create object action is logging """
        Person.objects.create(first_name="Vasilii",
                              last_name="Pupkin",
                              date_of_birthday="2014-02-01",
                              bio="Not very tall",
                              email="testemail@email.com",
                              jabber="",
                              skype="echo123",
                              other_contacts="No other contacts")

        last_action = DBActionsLog.objects.last()

        self.assertEqual(last_action.model, Person.__name__)
        self.assertEqual(last_action.action, 'created')

    def test_object_edited_action(self):
        """ Check if edit object action is logging """
        person = Person.objects.first()
        person.name = "Vasilii"
        person.save()

        last_action = DBActionsLog.objects.last()

        self.assertEqual(last_action.model, Person.__name__)
        self.assertEqual(last_action.action, 'updated')

    def test_object_deleted_action(self):
        """ Check if delete object action is logging """
        Person.objects.first().delete()

        last_action = DBActionsLog.objects.last()

        self.assertEqual(last_action.model, Person.__name__)
        self.assertEqual(last_action.action, 'deleted')


class TeamModelTest(TestCase):
    """
    Test the creation of new object in Person table
    """

    def create_team(self, name_of_the_team):
        return Team.objects.create(team_name=str(name_of_the_team))

    def test_team_creation(self):
        """
        Test if new object was created
        """
        team = self.create_team("42cc")
        team_unicode = (team.team_name)
        self.assertTrue(isinstance(team, Team))
        self.assertEqual(team.__unicode__(), team_unicode)

    def test_add_new_member(self):
        """
        Test if new member could be added to the team
        """
        team = self.create_team("42cc")
        member = Person.objects.first()
        team.team_members.add(member)
        self.assertTrue(isinstance(team.team_members.all()[0], Person))
        self.assertEqual(team.team_members.all()[0].__unicode__(),
                         member.__unicode__())

    def test_add_multiple_members(self):
        """
        Test if multiple members could be added to the team
        """
        team = self.create_team("42cc")

        for i in range(0, NUMBER_OF_MEMBERS):
            Person.objects.create(
                first_name="Vasilii" + str(i),
                last_name="Pupkin" + str(i),
                date_of_birthday="2014-02-01",
                bio="Not very tall" + str(i),
                email="testemail@email.com",
                jabber="" + str(i),
                skype="echo123" + str(i),
                other_contacts="No other contacts" + str(i)
            )

        members = Person.objects.all()
        team.team_members.add(*members)
        self.assertEqual(members.count(), team.team_members.all().count())

    def test_add_one_person_to_multiple_teams(self):
        """
        Test if one person could belongs to multiple teams
        """
        for i in range(0, NUMBER_OF_TEAMS):
            self.create_team("42cc"+str(i))

        teams = Team.objects.all()
        member = Person.objects.first()
        member.team_set.add(*teams)

        for team in teams:
            self.assertTrue(isinstance(team.team_members.all()[0], Person))
            self.assertEqual(team.team_members.all()[0].__unicode__(),
                             member.__unicode__())
