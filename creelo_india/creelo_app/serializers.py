from rest_framework import serializers
from .models import Product,ProductAttribute,ProductImage
from master_config.models import Category
from .models import Cart, CartItem, Product,ProductAttribute

class AttributeSerializer(serializers.Serializer):
    attribute_name = serializers.CharField(max_length=255, required=False, allow_blank=True, allow_null=True)
    attribute_value = serializers.CharField(max_length=255, required=False, allow_blank=True, allow_null=True)

class ProductImageSerializer(serializers.ModelSerializer):
    # image = serializers.ImageField(required=True)
    class Meta:
        model = ProductImage
        fields = ['image', 'added_by']

class ProductSerializer(serializers.ModelSerializer):
    attributes = AttributeSerializer(many=True, required=False, write_only=True)
    product_images = ProductImageSerializer(many=True, required=False, write_only=True)

    class Meta:
        model = Product
        fields = [
            'name', 'category', 'description', 'price', 'stock', 'rating', 'reviews',
            'is_featured_product', 'is_top_selling_product', 'is_new_arrivals', 'is_instock',
            'created_at', 'attributes', 'product_images'
        ]

    def create(self, validated_data):
        # Extract attributes and images from the validated data
        attributes_data = validated_data.pop('attributes', [])
        product_images_data = validated_data.pop('product_images', [])

        # Create the main product instance
        product = Product.objects.create(**validated_data)

        # Create associated ProductAttribute instances
        for attribute_data in attributes_data:
            ProductAttribute.objects.create(product=product, **attribute_data)

        # Create associated ProductImage instances
        for image_data in product_images_data:
            ProductImage.objects.create(product=product, **image_data)

        return product



class GetProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ['attribute_name', 'attribute_value']


class GetProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image', 'image_link']


class GetProductSerializer(serializers.ModelSerializer):
    attributes = GetProductAttributeSerializer(many=True, read_only=True) 
    images = GetProductImageSerializer(many=True, read_only=True)  
    class Meta:
        model = Product
        fields = [
            'name',
            'category',
            'description',
            'price',
            'stock',
            'rating',
            'reviews',
            'is_featured_product',
            'is_top_selling_product',
            'is_new_arrivals',
            'is_instock',
            'created_at',
            'attributes',  # Matches the `related_name` in `ProductAttribute`
            'images',  # Matches the `related_name` in `ProductImage`
        ]



class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', read_only=True, max_digits=10, decimal_places=2)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_name', 'product_price', 'quantity', 'get_total_price']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price']

    def get_total_price(self, obj):
        return sum(item.get_total_price() for item in obj.items.all())    