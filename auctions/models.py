from distutils.command.upload import upload
from email.policy import default
from unicodedata import category
from django.contrib.auth.models import AbstractUser
from django.db import models




#https://stackoverflow.com/questions/63497844/adding-items-to-wishlist-django
# This link explains how to make a wishlist (optional and self reference for future in this project)


class User(AbstractUser):
    pass


class Category(models.Model):
    categoryName = models.CharField(max_length = 30)
    def __str__(self):
        return self.categoryName
    


class Listing(models.Model):
    title = models.CharField(max_length = 30)
    description = models.CharField(max_length = 300)
    image = models.CharField(max_length = 3000, blank = True)
    price = models.FloatField()
    isActive = models.BooleanField(default = True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name = "owner")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name = "category")
    def __str__(self):
        return self.title


class Comment(models.Model):
    commentContent = models.CharField(max_length = 300)
    listings = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, related_name = "listings_comment")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name = "usercomment")
    def __str__(self):
        return f"{self.user}: {self.listings} / {self.commentContent}"


class Bid(models.Model):
    bidAmount = models.FloatField() 
    listings = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, related_name = "listings_bid")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name = "userbid")
    def __str__(self):
        return f"{self.user}: {self.listings} / {self.bidAmount}"


