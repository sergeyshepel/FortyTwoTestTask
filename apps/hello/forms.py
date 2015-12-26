# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.forms import ModelMultipleChoiceField
from django.forms.widgets import Textarea, SelectMultiple

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
    teams = ModelMultipleChoiceField(
        queryset=Team.objects.all(),
        widget=SelectMultiple(attrs={'size': '10'}),
        required=False
    )

    def __init__(self, *args, **kwargs):

        if 'instance' in kwargs:
            initial = kwargs.setdefault('initial', {})
            initial['teams'] = [team.pk
                                for team in kwargs['instance'].team_set.all()]

        ModelForm.__init__(self, *args, **kwargs)

        super(PersonForm, self).__init__(*args, **kwargs)

        for field in iter(self.fields):
            if field != 'person_pic':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control'
                })

    def save(self, commit=True):
        instance = ModelForm.save(self, False)

        old_save_m2m = self.save_m2m

        def save_m2m():
            old_save_m2m()
            instance.team_set.clear()
            for team in self.cleaned_data['teams']:
                instance.team_set.add(team)
        self.save_m2m = save_m2m

        if commit:
            instance.save()
            self.save_m2m()

        return instance


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
