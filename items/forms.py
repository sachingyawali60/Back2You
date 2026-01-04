from django import forms
from .models import Item, Claim
from django.contrib.auth.models import User

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'location', 'status', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'placeholder': 'Describe proof of ownership...',
                'rows': 4
            })
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']