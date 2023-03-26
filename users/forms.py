from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Skill, Message


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label="Name", widget=forms.TextInput(attrs={"class": 'input'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": 'input'}))
    username = forms.CharField(widget=forms.TextInput(attrs={"class": 'input'}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"class": 'input'}))
    password2 = forms.CharField(label="Password Confirmation", widget=forms.PasswordInput(attrs={"class": 'input'}))

    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        # labels = {
        #     'first_name': 'Name'
        # }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'username', 'email', 'short_intro', 'bio', 'location', 'profile_image',
                  'website_link', 'youtube_link', 'github_link', 'linkedin_link', 'twitter_link',
                  ]

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'message_title', 'body']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
