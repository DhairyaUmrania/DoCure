from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User,Cbc,ConfirmDoctor
from django.contrib.auth.hashers import make_password

# you have to pass string as parameter
password = "123"
make_password(password)

    
class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username= forms.CharField(label='Usename', 
                    widget=forms.TextInput(attrs={'placeholder': 'Enter your username'}))
    first_name= forms.CharField(label='First_name', 
                    widget=forms.TextInput(attrs={'placeholder': 'Enter your Firstname'}))
    last_name= forms.CharField(label='Last_name', 
                    widget=forms.TextInput(attrs={'placeholder': 'Enter your Lastname'}))
    email= forms.CharField(label='Email', 
                    widget=forms.TextInput(attrs={'placeholder': 'Enter your Email-id'}))
    age= forms.IntegerField(label='Age', 
                    widget=forms.TextInput(attrs={'placeholder': 'Enter your Age'}))
    height= forms.IntegerField(label='Height', 
                    widget=forms.TextInput(attrs={'placeholder': 'Enter your Height in CM'}))
    weight= forms.IntegerField(label='Weight', 
                    widget=forms.TextInput(attrs={'placeholder': 'Enter your Weight in Kg'}))
    
    

    class Meta:
        model = User
        fields = ("username","first_name",'last_name', "email", "password1", "password2","age","height","weight","gender")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class ConfirmDoctor(forms.ModelForm):
    class Meta:
        model = ConfirmDoctor
        fields = ('username','password','gender','Specialization','email')
    

from .models import Doctor
class DoctorForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    username= forms.CharField(label='Name', 
                    widget=forms.TextInput(attrs={'placeholder': 'Enter your username'}))
    Surname= forms.CharField(label='Surname', 
                    widget=forms.TextInput(attrs={'placeholder': 'Enter your Surname'}))
    email= forms.CharField(label='Email', 
                    widget=forms.TextInput(attrs={'placeholder': 'Enter your Email-id'}))
    phone_number= forms.CharField(label='phonenumber', 
                    widget=forms.TextInput(attrs={'placeholder': 'Enter your Correct Phone Number'}))
   
    
    
    # password = forms.CharField(widget=forms.PasswordInput)


    class Meta:
        model = Doctor
        fields = ('username','Surname', 'email','gender','phone_number','Specialization')
    def save(self, commit=True):
        user = super(DoctorForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
class ConfirmForm(forms.ModelForm):
    class Meta:
        model = Cbc
        fields = ("rbc","wbc","pc","hgb","rcd","mchc","mpv","pcv","mcv")
class EditProfile(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username","first_name",'last_name', "email", "age","height","weight","gender")