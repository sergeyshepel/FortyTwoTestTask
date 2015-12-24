from django.contrib import admin
from .models import Person, Requests, DBActionsLog, Team


admin.site.register(Person)
admin.site.register(Requests)
admin.site.register(DBActionsLog)
admin.site.register(Team)
