# -*- coding: utf-8 -*-
import json

from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers

from hello.models import Person, Requests


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
