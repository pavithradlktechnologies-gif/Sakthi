from django import forms
from admin_dashboard.models import *


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'project','message',]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full rounded-full border border-gray-200 bg-white px-4 py-3 text-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-900',
                'placeholder': 'Full Name',
            }),
            'email': forms.EmailInput(attrs={
                'type':'email',
                'class': 'w-full rounded-full border border-gray-200 bg-white px-4 py-3 text-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-900',
                'placeholder': 'Email Address',
            }),
            'phone': forms.TextInput(attrs={
                'type':'number',
                'class': 'w-full rounded-full border border-gray-200 bg-white px-4 py-3 text-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-900',
                'placeholder': 'Phone Number',
            }),
            'project': forms.Select(attrs={
                'class': 'w-full rounded-2xl border border-gray-200 bg-white px-4 py-3 text-gray-700 resize-none focus:outline-none focus:ring-2 focus:ring-gray-900',
            
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full rounded-2xl border border-gray-200 bg-white px-4 py-3 text-gray-700 resize-none focus:outline-none focus:ring-2 focus:ring-gray-900',
                'placeholder': 'Your Message',
                'rows': 5,
            }),
            
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
        if 'project' in self.fields:
            self.fields['project'].empty_label = "Select Project Name"
            current_choices = list(self.fields['project'].choices)
            current_choices.append(('0', 'Others'))
            self.fields['project'].choices = current_choices
# forms.py
class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = [
            "full_name", "email", "phone", "current_location",
            "professional_details", "total_experience",
            "highest_qualification", "notice_period", "resume"
        ]

        widgets = {
            "full_name": forms.TextInput(attrs={"class": "input"}),
            "email": forms.EmailInput(attrs={"class": "input"}),
            "phone": forms.TextInput(attrs={"class": "input"}),
            "current_location": forms.TextInput(attrs={"class": "input"}),
            "professional_details": forms.Textarea(attrs={"class": "textarea"}),
            "total_experience": forms.TextInput(attrs={"class": "input"}),
            "highest_qualification": forms.TextInput(attrs={"class": "input"}),
            "notice_period": forms.TextInput(attrs={"class": "input"}),
        }