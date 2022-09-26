from django.db import models
from category.models import Category
from django.urls import reverse
from accounts.models import Account 
from django.db.models import Avg, Count




class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    # whenever we delete a category the products under the category will be deleted
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name

    def averageReview(self):
        review = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if review['average'] is not None:
            avg = float(review['average'])
        return avg

    def countReview(self):
        review = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if review['count'] is not None:
            count = int(review['count'])
        return count

class ReviewRating(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200, unique=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)


    def __str__(self):
        return self.subject

    
# class ProductGallery(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to="store/products", max_length=255)

#     def __str__(self):
#         return self.product.product_name

#     class Meta:
#         verbose_name = 'productgallery'
#         verbose_name_plural = 'Product Gallery'



class FeaturesByProduct(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    line1 = models.TextField(max_length=40 , blank=True, null=True)
    line2 = models.TextField(max_length=40 , blank=True, null=True)
    line3 = models.TextField(max_length=40 , blank=True, null=True)
    line4 = models.TextField(max_length=40 , blank=True, null=True)

    
    class Meta:
        verbose_name = 'Feature'
        verbose_name_plural = 'Features'





    # class Features(models.Model):
    # line1 = models.TextField(max_length=40 , blank=True, null=True)
    # line2 = models.TextField(max_length=40 , blank=True, null=True)
    # line3 = models.TextField(max_length=40 , blank=True, null=True)
    # line4 = models.TextField(max_length=40 , blank=True, null=True)

    
    # class Meta:
    #     verbose_name = 'Feature'
    #     verbose_name_plural = 'Features'
    