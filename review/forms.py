from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from . import models


class LoginForm(forms.Form):
    username = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Nom d\'utilisateur'})
        )
    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'})
        )


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        help_texts = {
            'username': None,
        }

        labels = {
            'username': ''
        }

        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Nom d\'utilisateur'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password1'].label = ''
        self.fields['password1'].widget.attrs['placeholder'] = 'Mot de passe'
        self.fields['password2'].help_text = None
        self.fields['password2'].label = ''
        placeholder2 = 'Confirmer le mot de passe'
        self.fields['password2'].widget.attrs['placeholder'] = placeholder2


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
            'rating': forms.RadioSelect(choices=CHOICES),
            'headline': forms.TextInput(attrs={'placeholder': 'Titre'}),
            'body': forms.TextInput(attrs={'placeholder': 'Commentaire'})
        }

        labels = {
            'rating': 'Évaluation',
            'headline': '',
            'body': ''
        }


class CreateTicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        exclude = [
            'user',
            'time_created',
            ]

        labels = {
            'title': '',
            'description': ''
        }

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Titre'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description'})
        }


class UserFollowForm(forms.Form):

    to_follow = forms.CharField(
        max_length=180,
        required=False,
        label='',
        widget=forms.TextInput(
            attrs={'placeholder': 'Nom d\'utilisateur'}
        )
        )
