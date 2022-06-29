from dataclasses import fields
from django import forms
from .models import Movie, UserProfile,User



class movieform(forms.ModelForm):
    
    class Meta:
        model=Movie
        fields="__all__"
        
class Userform (forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','password','email']
     
        
class UserProfileForm(forms.ModelForm):
    role1=[('customer','customer'),('admin','admin')]
    role=forms.ChoiceField(widget=forms.RadioSelect(),choices=role1)
    
    class Meta:
        model = UserProfile
        fields = ['location', 'number']
        