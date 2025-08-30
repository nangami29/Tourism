from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, UserUpdateForm
# Create your views here. 
# user registration
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created")
            return redirect ('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html',  {'form': form})


@login_required
def profile_view(request):
    if request.method =='POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
       
        if user_form.is_valid():
            user_form.save()
           
            messages.success(request, "Your profile has been updated successfully!")
            return redirect( "home")
         # handle password update securely
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 and password1 == password2:
            user_form.set_password(password1)  
            messages.success(request, "Password updated successfully!")
        
        
    else:
        user_form = UserUpdateForm(instance=request.user)
        
    return render(request, "registration/profile.html", {
        "user_form": user_form,
    })

# Login 

class UserLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user =True
    next_page = reverse_lazy('home')

class LogoutView(LogoutView):
    next_page = reverse_lazy('login')