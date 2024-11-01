from django.db import models
from master_config.models import Category
from accounts.models import User
# Create your models here.

class Product(models.Model):
    """Model representing a product associated with categories."""
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0.0)
    stock = models.PositiveIntegerField(default=0)
    rating=models.DecimalField(max_digits=10, decimal_places=2,default=0.0)
    reviews=models.PositiveBigIntegerField(null=True,blank=True)
    is_featured_product=models.BooleanField(default=False)
    is_top_selling_product=models.BooleanField(default=False)
    is_new_arrivals=models.BooleanField(default=False)
    is_instock=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)


    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['name']

    def __str__(self): 
        return self.name


class ProductAttribute(models.Model):
    """Model representing additional attributes for products like color, size, etc."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes')
    attribute_name = models.CharField(max_length=100,null=True,blank=True)
    attribute_value = models.CharField(max_length=255,null=True,blank=True)

    def __str__(self):
        return f"{self.attribute_name}: {self.attribute_value}"


class ProductImage(models.Model):
    """Model representing multiple images associated with a product."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/',null=True,blank=True)
    image_link=models.CharField(max_length=111,null=True,blank=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='added_images')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='updated_images')
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)



    def __str__(self):
        return f"Image for {self.product.name}"

