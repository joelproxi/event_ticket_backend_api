from datetime import datetime

from django import forms

from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'start_date', 'end_date', 'location', 'organizer']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'placeholder': 'Start Date', 'class': 'form-control'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'placeholder': 'End Date', 'class': 'form-control'}),
            'location': forms.TextInput(attrs={'placeholder': 'Event Location', 'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and start_date >= end_date:
            raise forms.ValidationError("End date must be after start date.")

        if start_date and start_date < datetime.now():
            raise forms.ValidationError("Start date cannot be in the past.")
        return cleaned_data