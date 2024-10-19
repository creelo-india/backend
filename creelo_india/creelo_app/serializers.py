from rest_framework import serializers
from .models import Product,ProductAttribute,ProductImage
from master_config.models import Category

#  product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
#     image = models.ImageField(upload_to='product_images/')
#     added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='added_images')
#     updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='updated_images')
#     created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
#     updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductImage
        fields=['id','image','added_by','image_link','created_at']



class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ['id', 'attribute_name', 'attribute_value']

class ProductSerializer(serializers.ModelSerializer):
    attributes = ProductAttributeSerializer(many=True, required=False)
    productimage=ProductImageSerializer(many=True,required=False)
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'description', 'price', 'stock','is_featured_product', 'is_top_selling_product','is_new_arrivals','created_at', 'attributes','productimage']

    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        return product
    
    def update(self, instance, validated_data):
        # Remove and process attributes separately
        attributes_data = validated_data.pop('attributes', [])

        # Update product fields
        instance.name = validated_data.get('name', instance.name)
        instance.category = validated_data.get('category', instance.category)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.stock = validated_data.get('stock', instance.stock)
        instance.save()

        # Update or create associated attributes
        for attribute_data in attributes_data:
            attribute_id = attribute_data.get('id')
            if attribute_id:
                # If attribute exists, update it
                attribute_instance = ProductAttribute.objects.get(id=attribute_id, product=instance)
                attribute_instance.attribute_name = attribute_data.get('attribute_name', attribute_instance.attribute_name)
                attribute_instance.attribute_value = attribute_data.get('attribute_value', attribute_instance.attribute_value)
                attribute_instance.save()
            else:
                # If no attribute ID, create a new attribute
                ProductAttribute.objects.create(product=instance, **attribute_data)

        return instance
    