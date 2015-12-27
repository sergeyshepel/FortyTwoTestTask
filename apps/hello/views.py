# -*- coding: utf-8 -*-
import json
import signals  # NOQA

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from django.core import serializers
from django.contrib.auth.decorators import login_required

from hello.models import Person, Requests
from hello.forms import PersonForm, TeamForm


def index(request):
    person = Person.objects.first()
    return render(request, 'hello/index.html', {'person': person})


def requests(request):
    if request.is_ajax():
        response_data = {}
        latest_id = request.GET.get('latest_id', 1)
        new_requests = Requests.objects.all(
        ).filter(pk__gt=latest_id)[:10]
        response_data['requests'] = serializers.serialize(
            "json", new_requests.reverse()
        )
        return HttpResponse(
            json.dumps(response_data),
            content_type='application/json'
        )
    ten_requests = Requests.objects.all()[:10]
    new_requests = sorted(ten_requests, key=lambda x: x.priority, reverse=True)
    return render(request,
                  'hello/requests.html',
                  {'new_requests': new_requests})


@login_required()
def edit(request, pk=None):
    person_obj = get_object_or_404(Person, pk=pk)
    person_form = PersonForm(request.POST or None,
                             request.FILES or None,
                             instance=person_obj)

    if request.is_ajax() and request.method == 'POST':
        if person_form.is_valid():
            response_data = {}
            try:
                person_form.save()
                response_data['msg'] = u'Record was updated successfully'
            except:
                response_data['msg'] = u'Failed to update the record'
            return HttpResponse(json.dumps(response_data),
                                content_type="application/json")
        return HttpResponseBadRequest(json.dumps(dict(person_form.errors)))
    return render(request, 'hello/edit.html', {'person_form': person_form})


@login_required()
def add_team(request):
    if request.is_ajax() and request.method == 'POST':
        team_form = TeamForm(request.POST)
        if team_form.is_valid():
            response_data = {}
            try:
                team_form.save()
                response_data['msg'] = u'Team was added successfully'
            except:
                response_data['msg'] = u'Failed to add team'
            return HttpResponse(json.dumps(response_data),
                                content_type="application/json")
        return HttpResponseBadRequest(json.dumps(dict(team_form.errors)))
    elif request.method == 'POST' or request.is_ajax():
        response_data = {}
        response_data['msg'] = u'Method not allowed!'
        return HttpResponseBadRequest(json.dumps(response_data),
                                      content_type="application/json")
    team_form = TeamForm()
    return render(request, 'hello/team.html', {'team_form': team_form})
