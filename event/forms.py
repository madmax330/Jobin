from django import forms
from .models import Event, SavedEvent

import datetime


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        exclude = ('active', 'schools', 'programs', 'times_saved',)

    def clean(self):
        clean_data = super(EventForm, self).clean()
        date = clean_data.get('start_date')
        if date < datetime.datetime.now().date():
            raise forms.ValidationError({'start_date': 'The event start date must be after today\'s date.'})
        end = clean_data.get('end_date')
        if end:
            if end < datetime.datetime.now().date():
                raise forms.ValidationError({'end_date': 'The event end date must be after today\'s date.'})
            if end < date:
                raise forms.ValidationError({'end_date': 'The event end date must be after the start date.'})


class NewSavedEventForm(forms.ModelForm):

    class Meta:
        model = SavedEvent
        fields = '__all__'




