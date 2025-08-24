from django.db import models
from django.contrib.auth.models import AbstractUser
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
    image= models.ImageField(upload_to='attractions/')
    def __str__(self):
        return f"{self.name} - {self.location}"
 # optimizing queries with prefetching
attraction = Attraction.objects.prefetch_related('category')

class Rating (models.Model):
    user_id = models.ForeignKey(CustomUser,  on_delete= models.CASCADE)
    attractions_id = models.ForeignKey(Attraction, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
