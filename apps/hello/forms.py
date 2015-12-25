# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.forms.widgets import Textarea

from hello.models import Person, Team
from hello.widgets import DataPickerWidget, UploadImageWidget


class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = '__all__'
        widgets = {
            'date_of_birthday': DataPickerWidget(
                params="dateFormat: 'yy-mm-dd', \
                        changeYear: true, defaultDate: 'c-25', \
                        yearRange: 'c-115:c'",
                attrs={'class': 'datepicker'}),
            'person_pic': UploadImageWidget,
            'bio': Textarea(attrs={'rows': '5'}),
            'other_contacts': Textarea(attrs={'rows': '5'}),
        }

    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            if field != 'person_pic':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control'
                })


class TeamForm(ModelForm):
    class Meta:
        model = Team
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TeamForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
