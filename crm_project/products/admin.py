from django.contrib import admin
from .models import Product, ProductImage, ProductSpecification, SerialNumber

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductSpecInline(admin.TabularInline):
    model = ProductSpecification
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['sku', 'name', 'brand', 'category', 'selling_price', 'status']
    inlines = [ProductImageInline, ProductSpecInline]

@admin.register(SerialNumber)
class SerialNumberAdmin(admin.ModelAdmin):
    list_display = ['serial_number', 'product', 'customer', 'status']
