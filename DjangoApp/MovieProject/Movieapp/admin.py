from django.contrib import admin
from .models import Movie, UserProfile, Cart

# Register your models here.
admin.site.register(Movie)
admin.site.register(UserProfile)
admin.site.register(Cart)