from django.urls import path
from .views import register_view, profile_view, UserLoginView, LogoutView, SignUpView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('register/', register_view, name ='register'),
    path ('login/', UserLoginView.as_view(template_name ='registration/login.html'), name='login'),
    path ('logout/', LogoutView.as_view(), name = 'logout'),
    path('profile/', profile_view, name='profile'),
]