from argparse import _MutuallyExclusiveGroup
from asyncio.windows_events import NULL
from email.policy import default
from itertools import product
from pickle import TRUE
from tkinter import CASCADE
from turtle import ondrag
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.html import mark_safe
from django.contrib import admin

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    nationaID = models.CharField(max_length=10, null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)
    mobilephone = models.CharField(max_length=11, null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)
    address = models.TextField(max_length=300, null=True, blank=True)
    birthDate = models.DateField(null=True, blank=True)
    postalCode = models.CharField(max_length=10, null=True, blank=True)
    cardNumber = models.CharField(max_length=24, blank=True, null=True)
    createDate = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class ShopCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    createDate = models.DateField(null=True)

    def __str__(self):
        return self.user.username + "'s Shopcart"


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    desciption = models.TextField(max_length=300, null=True, blank=True)
    category = models.ManyToManyField(Category)
    dkp = models.CharField(unique=True, max_length=12, null=True, blank=True)
    createDate = models.DateField(null=True)
    averageRating = models.IntegerField(null=True, blank=True)
    ratingCount = models.IntegerField(null=True, blank=True)
    cover = models.ImageField(
        upload_to='images/', default=None, blank=True, null=True)

    def __str__(self):
        return self.name

    def photo(self):
        return mark_safe('<img src="/mdeia/%s" width="90" height="90" />' % self.cover)


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.TextField(max_length=250)
    rate = models.IntegerField(null=True, blank=True)
    published = models.BooleanField(default=False)
    createDate = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'comment {self.user} on {self.product}'


class Gallery(models.Model):
    image = models.ImageField(
        upload_to='images/', default=None, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name + "'s image"

    def photo(self):
        return mark_safe('<img src="/image%s" width="90" height="90" />' % self.image)


class VariantProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    dkpc = models.CharField(unique=True, max_length=12, null=True, blank=True)
    size = models.IntegerField()
    mainPrice = models.IntegerField()
    discountPrice = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.product} -سایز {self.size}'


class CartItem(models.Model):
    shopCart = models.ForeignKey(ShopCart, on_delete=models.CASCADE)
    variantProduct = models.ForeignKey(
        VariantProduct, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    createDate = models.DateField(null=True)

    def __str__(self):
        return f'{self.shopCart}'+' cart item'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    createDate = models.DateField()
    informations = models.TextField(null=True)
    note = models.TextField(null=True, blank=True)


statuschoices = (('d', 'delivered'), ('o', 'onway'), ('r', 'refunded'))


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    variantProduct = models.ForeignKey(
        VariantProduct, null=True, on_delete=models.CASCADE)
    price = models.IntegerField(null=True, blank=True)
    status = models.CharField(choices=statuschoices,
                              max_length=10, default='o')


class PaymentDetails(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    amount = models.IntegerField()
    status = models.CharField(max_length=10)
    createDate = models.DateField()
