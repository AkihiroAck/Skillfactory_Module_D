from django.db import models
from django.contrib.auth.models import User
from mymodel.models import Category

# Create your models here.


class Subscriptions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subscriptions')
    
    def __str__(self):
        return f'{self.user.username} - {self.category.name}'
    