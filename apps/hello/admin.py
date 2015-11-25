from django.contrib import admin
from .models import Person, Requests, DBActionsLog


admin.site.register(Person)
admin.site.register(Requests)
admin.site.register(DBActionsLog)
