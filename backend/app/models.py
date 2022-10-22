from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass

class Business(models.Model):
    name = models.CharField(max_length = 500, unique = True)
    logo_url = models.CharField(max_length = 1000,)
    owner = models.ForeignKey(User, on_delete = models.CASCADE, blank = True)
    description = models.TextField()

    def __str__(self):
        return self.name
class Category(models.Model):
    name  = models.CharField(max_length = 200)

    def __str__(self):
        return self.name    

class Item(models.Model):
    name = models.CharField(max_length = 500)
    business = models.ForeignKey(Business, on_delete = models.CASCADE, blank = True)
    price = models.PositiveIntegerField()
    description = models.TextField()
    picture_url = models.CharField(max_length = 1000)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, blank = True, null = True)

    def __str__(self):
        return f"{self.business} item: {self.name}"

class Order(models.Model):
    item = models.ForeignKey(Item, on_delete = models.CASCADE) #one item
    user_from = models.CharField(max_length = 500) #holds the usernamem of the user that made the order
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.PositiveIntegerField()
    active = models.BooleanField(default = False)
    fulfilled = models.BooleanField(default = False)

    def __str__(self):
        return f"order_id: {self.pk}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, )
    orders = models.ManyToManyField(Order, blank = True)
    total = models.PositiveIntegerField()

    def __str__(self):
        return f"cart for {self.user}"
