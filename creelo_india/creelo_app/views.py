from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Product,ProductAttribute,ProductImage
from .serializers import ProductSerializer
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Cart, CartItem, Product
from .serializers import CartSerializer, CartItemSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # You can override the create method to customize the logic
    def create(self, request, *args, **kwargs):
        # Extract attributes from request data if present
        attributes_data = request.data.pop('attributes', []) 
        product_images=request.data.pop('productimage',[])       
        # Validate product data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Save product
        self.perform_create(serializer)
        product = serializer.instance  
        # Handle product attributes
        for attribute_data in attributes_data:
            ProductAttribute.objects.create(product=product, **attribute_data)
        # login_user=1
        for product_image in product_images:
            ProductImage.objects.create(product=product,**product_image)
        serializer = self.get_serializer(product)
        print("again reload the product data ")
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    # Optional: You can customize perform_create or perform_update if needed
    # def perform_create(self, serializer):
    #     print("second called here   ")
    #     serializer.save()

    def perform_update(self, serializer):
        serializer.save()

# Utility function to get or create a cart for the user
def get_user_cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart

# View to add a product to the cart
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_to_cart(request):
    try:
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        # Validate that product exists
        product = Product.objects.get(id=product_id)
        # Get the user's cart
        cart = get_user_cart(request.user)
        # Check if the product is already in the cart
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:  # If the item already exists in the cart, update the quantity
            cart_item.quantity += quantity
            cart_item.save()
        else:
            cart_item.quantity = quantity
            cart_item.save()
        return Response({"message": "Product added to cart."}, status=status.HTTP_201_CREATED)
    except Product.DoesNotExist:
        return Response({"error": "Product not found."}, status=status.HTTP_400_BAD_REQUEST)

# View to retrieve the user's cart
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_cart(request):
    cart = get_user_cart(request.user)
    serializer = CartSerializer(cart)
    return Response(serializer.data)        
