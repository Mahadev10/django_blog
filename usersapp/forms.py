from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.core.exceptions import ValidationError
from usersapp.models import UserProfile


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label="firstname",min_length=3,max_length=150)
    last_name = forms.CharField(label="lastname",required=False)
    email = forms.EmailField(label="Email")
    profile_photo = forms.ImageField(label="Profile Photo",required=False)
    class Meta:
        model=UserProfile
        fields = ("username","email","profile_photo")
    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        user = UserProfile.objects.filter(username=username)
        if user.count():
            raise ValidationError("User Already Exists")
        return username
    def clean_email(self):
        email=self.cleaned_data['email'].lower()
        user=UserProfile.objects.filter(email=email)
        if user.count():
            raise ValidationError("Email Already Exists")
        return email    
    def save(self,commit=True):
        user = UserProfile.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1'],
        )
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.profile_photo = self.cleaned_data['profile_photo']
        user.save()
        return user