from django import forms
from .models import Event, SavedEvent

import datetime


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        exclude = ('active', 'schools', 'programs', 'times_saved',)

    def clean(self):
        clean_data = super(EventForm, self).clean()
        date = clean_data.get('date')
        if date < datetime.datetime.now().date():
            raise forms.ValidationError({'date': 'The event date must be after today\'s date.'})


class NewSavedEventForm(forms.ModelForm):

    class Meta:
        model = SavedEvent
        fields = '__all__'




