from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, DeleteView, DetailView, UpdateView
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, UserUpdateForm
from . models import Attraction, Rating
from .forms import AttractionForm, RatingForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from taggit.models import Tag
from django.db.models import Q
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
class HomeView(ListView):
    model = Attraction
    template_name = "nakuru_tourism_app/home.html"
    context_object_name = "attractions"
    ordering = ['-created_at']

class TourismListView(ListView):
    model = Attraction
    template_name = 'attractions/attraction_list.html'
    context_object_name = 'attraction_list'
    ordering = ['-created_at']

    def get_queryset(self):
        qs = super().get_queryset()
        print(qs)  
        return qs

class AttractionCreateView( LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Attraction
    form_class = AttractionForm
    template_name = "attractions/create_attrations.html"
    success_url = reverse_lazy('attraction_list')

    def test_func(self):
        return self.request.user.is_staff

class AttractionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model =Attraction
    fields = ['location', 'description', 'longitude',' latitude', 'entry_fee',
              'opening_hours', 'image']
    template_name = 'attractions/ update.html'
    success_url = reverse_lazy('attraction_list')

    def form_valid(self, form):
        #Runs after the form is validated and before saving.
        form.instance.author = self.request.user
        response = super().form_valid(form)
        return response
    def test_func(self):
        return self.request.user.is_staff
class AttractionDetailView(DetailView):
    model = Attraction
    template_name = 'attractions/attraction_detail.html'
    context_object_name = 'attraction'


# delete an attraction
class AttractionDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Attraction 
    template_name = 'attractions/ delete.html'
    success_url =reverse_lazy('attraction_list')

    def test_func(self):
        return self.request.user.is_staff
    

    #CRUD for rating
class RatingCreateView(LoginRequiredMixin, CreateView):
    model = Rating
    form_class = RatingForm
    template_name ='ratings/rating_form.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.attraction =  get_object_or_404(Attraction, pk=self.kwargs['pk'])
        return super().form_valid(form)

    
    def get_success_url(self):
        return self.object.attraction.get_absolute_url()
class RatingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Rating
    form_class = RatingForm
    template_name = "ratings/rating_form.html"

    def test_func(self):
        rating = self.get_object()
        return self.request.user == rating.user

    def get_success_url(self):
        return reverse_lazy("attraction_detail", kwargs={"pk": self.object.attraction.pk})

def attraction_detail(request, pk):
    attraction = get_object_or_404(Attraction, pk=pk)
    ratings = attraction.ratings.all()  
    return render(request, "attractions/attraction_detail.html", {
        "attraction": attraction,
        "ratings": ratings
    })
class RatingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Rating
    template_name = "ratings/rating_confirm_delete.html"

    def test_func(self):
        rating = self.get_object()
        return self.request.user == rating.user

    def get_success_url(self):
        return reverse_lazy("attraction_detail", kwargs={"pk": self.object.attraction.pk})
    
class HomeView(TemplateView):
    template_name = "nakuru_tourism_app/home.html"

def attraction_by_tag (request, tag_name):
    tag =get_object_or_404(Tag, name=tag_name)
    attraction = Attraction.objects.filter(tags=tag)
    return render(request, 'attractions/attraction_by_tag.html', {'tag': tag, 'attraction':attraction})

def search_attractions(request):
    query = request.GET.get('q')
    results = []

    if query:
        results = Attraction.objects.filter(
            Q(name__icontains=query) |            
            Q(description__icontains=query) |   
            Q(location__icontains=query) |       
            Q(tags__name__icontains=query) |     
            Q(category__name__icontains=query)   
        ).distinct()

    return render(request, 'search_results.html', {'results': results, 'query': query})