from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Product,ProductAttribute,ProductImage
from .serializers import ProductSerializer,GetProductSerializer
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Cart, CartItem, Product
from .serializers import CartSerializer, CartItemSerializer

from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Product, ProductImage, ProductAttribute

from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        product_data = request.data.copy()

        # Dynamically gather all attribute data
        attributes_data = []
        i = 0
        while f'attributes[{i}][attribute_name]' in request.data:
            attribute_name = request.data.get(f'attributes[{i}][attribute_name]')
            attribute_value = request.data.get(f'attributes[{i}][attribute_value]')
            if attribute_name and attribute_value:
                attributes_data.append({
                    'attribute_name': attribute_name,
                    'attribute_value': attribute_value
                })
            i += 1
        product_images_data = []
        i = 0
        while f'productimage[{i}][image]' in request.FILES:
            image_field = f'productimage[{i}][image]'
            added_by_field = f'productimage[{i}][added_by]'

            if image_field in request.FILES:
                added_by = request.data.get(added_by_field, None)
                product_images_data.append({
                    'image': request.FILES[image_field],
                    'added_by': added_by
                })
            i += 1

        # Pass only the main product data to the serializer, without attributes and images
        main_product_data = {key: product_data[key] for key in product_data if not key.startswith('attributes') and not key.startswith('productimage')}
        serializer = self.get_serializer(data=main_product_data)

        if serializer.is_valid():
            # Save the main product instance
            product = serializer.save()

            # Manually save each attribute instance
            for attribute in attributes_data:
                ProductAttribute.objects.create(product=product, **attribute)
            
            # Manually save each product image instance
            for image_data in product_images_data:
                ProductImage.objects.create(product=product, **image_data)

            return Response({
                'message': 'Product created successfully!',
                'product': serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)




        
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


from rest_framework.response import Response
from rest_framework import status

class GetProductList(APIView):
    def get(self, request, *args, **kwargs):
        try:
            products = Product.objects.all()
            serializer = GetProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

