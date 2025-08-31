from django import forms 
from .models import CustomUser
from taggit.forms import TagWidget
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser,  Attraction, Category, Rating, Tag
# Custom user registration form
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'password1', 'password2']

# Login form
class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role']


# Category form
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


# Attraction form
class AttractionForm(forms.ModelForm):
    class Meta:
        model = Attraction
        fields = [
            'name', 'description', 'location', 'latitude', 'longitude',
            'entry_fee', 'opening_hours', 'category', 'image', 'tags'
        ]
        widgets ={
            'tags': TagWidget(),
        }


# Rating form
class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['attraction', 'score', 'comment']

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields =['name']