
from email.policy import default
from django.db import models
from django.contrib.auth.models import User,Group

# Create your models here.

class Movie(models.Model):
    name=models.CharField(max_length=20)
    certificate=models.CharField(choices=[('U/A','U/A'),('A','A')],max_length=3)
    type=models.CharField(max_length=10)
    language=models.CharField(max_length=10)
    duration=models.CharField(max_length=20)
    director=models.CharField(max_length=20)
    cast=models.CharField(max_length=50)
    description=models.CharField(max_length=1000)
    #select_date=models.DateField()
    #select_time=models.TimeField()
    Price=models.IntegerField()
    Image=models.ImageField(upload_to='media')
    
    #select_date_and_time=models.DateField(auto_now_add=True)
    
    
    class Meta:
        db_table='movie'
        
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    location = models.CharField(max_length=20)
    number = models.IntegerField()
    
    class Meta:
        db_table='UserProfile'
        
        
admin, status = Group.objects.get_or_create(name='admin')
customer, status = Group.objects.get_or_create(name='customer')

class Cart(models.Model):
    movieobject=models.ForeignKey(Movie,on_delete=models.CASCADE)
    userObject=models.ForeignKey(User,on_delete=models.CASCADE)
    number_of_ticket=models.IntegerField(default=1)
    totalprice=models.FloatField()
    
    class Meta:
        db_table='cart'
    def __str__(self) :
        return str(self.userObject)