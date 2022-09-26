from django.contrib import admin
from .models import Product, ReviewRating, FeaturesByProduct


    


# class ProductGalleryInline(admin.TabularInline):
#     model = ProductGallery
#     extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display    = ('product_name', 'price', 'stock','category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug':('product_name',)}




admin.site.register(Product, ProductAdmin)
admin.site.register(ReviewRating)
# admin.site.register(ProductGallery)
admin.site.register(FeaturesByProduct)