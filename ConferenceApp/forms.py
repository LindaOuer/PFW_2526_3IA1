from django import forms
from .models import Conference

class ConferenceForm(forms.ModelForm):
    class Meta:
        model = Conference
        fields = ['theme',  'name', 'start_date', 'end_date', 'location', 'description']
        labels = {
            'name': 'Conference Name',
            'theme': 'Conference Theme',
            'start_date': 'Start Date',
            'end_date': 'End Date',
            'location': 'Location',
            'description': 'Description',
        }
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows':4, 'cols':15, 'placeholder': 'Enter conference description here...'}),
        }