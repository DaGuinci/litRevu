from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from . import models


class LoginForm(forms.Form):
    username = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder':'Nom d\'utilisateur'})
        )
    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'placeholder':'Mot de passe'})
        )


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        help_texts = {
            'username': None,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

class CreateReviewForm(forms.ModelForm):
    class Meta:
        CHOICES = [
            ('1', 1),
            ('2', 2),
            ('3', 3),
            ('4', 4),
            ('5', 5),
        ]
        model = models.Review
        exclude = [
            'user',
            'ticket'
            ]
        widgets = {
            "rating": forms.RadioSelect(choices=CHOICES)
        }


class CreateTicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        exclude = [
            'user',
            'time_created',
            ]