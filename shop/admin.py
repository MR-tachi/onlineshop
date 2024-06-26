from itertools import product
from django.contrib import admin
from shop.models import *
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['category']
    search_fields = ['name']
    list_display = ['photo', 'name']


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']


class GalleryAdmin(admin.ModelAdmin):
    list_display = ['photo','__str__']


admin.site.register(Profile)
admin.site.register(ShopCart)
admin.site.register(Review)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(VariantProduct)
admin.site.register(Gallery,GalleryAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(PaymentDetails)
admin.site.register(CartItem)
