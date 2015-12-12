# -*- coding: utf-8 -*-
import json
import signals  # NOQA

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from django.core import serializers
from django.contrib.auth.decorators import login_required

from hello.models import Person, Requests
from hello.forms import PersonForm


def index(request):
    person = Person.objects.first()
    return render(request, 'hello/index.html', {'person': person})


def requests(request):
    if request.is_ajax():
        response_data = {}
        latest_id = request.GET.get('latest_id', 1)
        new_requests = Requests.objects.all(
        ).order_by('-time').filter(pk__gt=latest_id).reverse()
        response_data['requests'] = serializers.serialize(
            "json", new_requests[:10]
        )
        response_data['requests_quantity'] = len(new_requests)
        return HttpResponse(
            json.dumps(response_data),
            content_type='application/json'
        )
    new_requests = Requests.objects.all().order_by('-time')[:10]
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
