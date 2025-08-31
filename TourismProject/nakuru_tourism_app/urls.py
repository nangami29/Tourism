from django.urls import path
from .views import register_view, profile_view, UserLoginView, LogoutView, SignUpView
from .views import (
    TourismListView, AttractionDetailView,
    AttractionCreateView, AttractionUpdateView, AttractionDeleteView,
    RatingCreateView, RatingUpdateView, RatingDeleteView,
)
from . import views

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('register/', register_view, name ='register'),
    path ('login/', UserLoginView.as_view(template_name ='registration/login.html'), name='login'),
    path ('logout/', LogoutView.as_view(), name = 'logout'),
    path('profile/', profile_view, name='profile'),

 
    path('attractions/', TourismListView.as_view(), name='attraction_list'),
    path('attractions/<int:pk>/', AttractionDetailView.as_view(), name='attraction_detail'),
    path('attractions/create/', AttractionCreateView.as_view(), name='attraction_create'),
    path('attractions/<int:pk>/update/', AttractionUpdateView.as_view(), name='attraction_update'),
    path('attractions/<int:pk>/delete/', AttractionDeleteView.as_view(), name='attraction_delete'),

    path('attractions/<int:pk>/rate/', RatingCreateView.as_view(), name='rating_create'),
    path('ratings/<int:pk>/edit/', RatingUpdateView.as_view(), name='rating_update'),
    path('ratings/<int:pk>/delete/', RatingDeleteView.as_view(), name='rating_delete'),
    path('tags/<slug:tag_slug>/', views.attraction_by_tag, name='attraction by tag'),
    path('search/', views.search_attractions, name='search Tourist Attractions'),
]
