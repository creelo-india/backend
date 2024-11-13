from rest_framework import serializers
from .models import Product,ProductAttribute,ProductImage
from master_config.models import Category
from .models import Cart, CartItem, Product,ProductAttribute

#  product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
#     image = models.ImageField(upload_to='product_images/')
#     added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='added_images')
#     updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='updated_images')
#     created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
#     updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)

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
    productimage = ProductImageSerializer(many=True, required=False, write_only=True)

    class Meta:
        model = Product
        fields = [
            'name', 'category', 'description', 'price', 'stock',
            'is_featured_product', 'is_top_selling_product', 'is_new_arrivals', 'is_instock',
            'attributes', 'productimage'
        ]

    def create(self, validated_data):
        # Extract attributes and product images from validated data
        attributes_data = validated_data.pop('attributes', [])
        product_images_data = validated_data.pop('productimage', [])

        # Create the Product instance
        product = Product.objects.create(**validated_data)

        # Create ProductAttribute instances
        ProductAttribute.objects.bulk_create(
            [ProductAttribute(product=product, **attr_data) for attr_data in attributes_data]
        )

        # Create ProductImage instances
        ProductImage.objects.bulk_create(
            [ProductImage(product=product, **img_data) for img_data in product_images_data]
        )

        return product




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