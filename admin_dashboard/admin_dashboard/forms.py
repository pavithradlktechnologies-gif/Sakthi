from django import forms
from .models import *
from django_ckeditor_5.widgets import CKEditor5Widget



class BannerVideoForm(forms.ModelForm):
    class Meta:
        model = Banner_video
        fields = '__all__'

        widgets = {
            'video': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'video/*'
            })
        }




class BlogPostForm(forms.ModelForm):
    content = forms.CharField(
        widget=CKEditor5Widget(config_name='default'),
        required=False
    )
    class Meta:
        model = BlogPost
        fields = [
            'title',
            'content',
            'image',
            'video_url',
            'published_at',

            'meta_title',
            'meta_description',
            'show_cta',
            'cta_text',
            'cta_link',
            'comment_show_status'
        ]


        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'video_url': forms.URLInput(attrs={'class': 'form-control'}),
            'published_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'meta_title': forms.TextInput(attrs={'class': 'form-control'}),
            'meta_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'show_cta': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'cta_text': forms.TextInput(attrs={'class': 'form-control'}),
            'cta_link': forms.URLInput(attrs={'class': 'form-control'}),
            'comment_show_status' : forms.CheckboxInput(attrs={'class': 'form-check-input','type':'checkbox'}),
        }



 
class CareerForm(forms.ModelForm):
    class Meta:
        model = Career
        fields = "__all__"

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter job title",
            }),
            "location": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Job location",
            }),
            "job_type": forms.Select(attrs={
                "class": "form-select",
            }),
            "category": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Job category e.g., Engineering, Marketing",
            }),
            "experience_required": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g., 0–2 years",
            }),
            "salary_range": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Optional (e.g., Will be discussed)",
            }),
            "job_summary": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Short description of the job",
            }),
            "roles_responsibilities": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "List the roles & responsibilities...",
            }),
            "skills_required": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Required job skills...",
            }),
            "status": forms.Select(attrs={
                "class": "form-select",
            }),
        }

