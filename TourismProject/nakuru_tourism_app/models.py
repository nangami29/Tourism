from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from taggit.managers import TaggableManager

# Integrate Tagging Functionality
class Tag(models.Model):
    name = models.CharField(max_length = 50, unique=True)

    def __str__(self):
        return self.name
    
# Create your models here.
class CustomUser (AbstractUser):
   Role_CHOICES = (
       ('admin', 'admin'),
       ('user', 'user'),
   )
   role = models.CharField(max_length=10, choices=Role_CHOICES, default='user')

   def __str__(self):
       return f"{self.username} ({self.role})"
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
    
class Attraction (models.Model):
    
    name= models.CharField(max_length=200)
    description =models.TextField()
    location= models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    entry_fee= models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    opening_hours =models.CharField (max_length=50, null=True, blank=True)
    created_at= models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='attractions')
    image= models.ImageField(upload_to='attractions/', blank=True)
    tags =TaggableManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("attraction_detail", kwargs={"pk": self.pk})
class Rating (models.Model):
    user = models.ForeignKey(CustomUser,  on_delete= models.CASCADE)
    attraction= models.ForeignKey(Attraction, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField(choices=[(i, i) for i in range (1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    
    def __str__(self):
        return f"{self.attraction.name} - {self.stars} stars"
