# -*- coding: utf-8 -*-
from django.shortcuts import render

from hello.models import Person


def index(request):
    person = Person.objects.first()
    return render(request, 'hello/index.html', {'person': person})
