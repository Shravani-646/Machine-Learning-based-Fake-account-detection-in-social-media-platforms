from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm,NumberInput,ChoiceField,TextInput
from .models import FeatureSet,CloneFeatureSet,UserInput
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder':('Username')})
        self.fields['email'].widget.attrs.update({'placeholder':('Email Address')})
        self.fields['password1'].widget.attrs.update({'placeholder':('Password')})        
        self.fields['password2'].widget.attrs.update({'placeholder':('Confirm Password')})
    

class FeatureSetForm(ModelForm):
    language = ChoiceField(choices=FeatureSet().LANGUAGE_CHOICES)
    
    class Meta:
        model = FeatureSet
        fields = ['statuses_count','followers_count','friends_count','favourites_count','listed_count','geo_enabled',
                  'user_profile_background_image','language']
        
        widgets = {
            'statuses_count': NumberInput(attrs={
                'class': "form-control",
                'placeholder': 'Eg-25'
                }),
            'followers_count': NumberInput(attrs={
                'class': "form-control", 
                'placeholder': 'Eg-4'
                }),
            'friends_count': NumberInput(attrs={
                'class': "form-control",
                'placeholder': 'Eg-788'
                }),
            'favourites_count': NumberInput(attrs={
                'class': "form-control",
                'placeholder': 'Eg-14'
                }),
            'listed_count': NumberInput(attrs={
                'class': "form-control",
                'placeholder': 'Eg-2'
                }),
            
        }



class CloneFeatureSetForm(ModelForm):
    language = ChoiceField(choices=FeatureSet().LANGUAGE_CHOICES)
    
    class Meta:
        model = CloneFeatureSet
        fields = ['name','screen_name','language','location']

        widgets = {
            'name': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'David Stellmen'
                }),
            'screen_name': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'AskDavid'
                }),
            'location': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Cleveland,Ohio'
                }),
            
        }

class UserInputForm(ModelForm):
    class Meta:
        model = UserInput
        fields = "__all__"
        widgets = {
            'profile_url': TextInput(attrs={
                'class': "form-control",
                }),
        }
        
        
        


