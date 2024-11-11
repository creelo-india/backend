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

from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Product, ProductImage, ProductAttribute

from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework.parsers import MultiPartParser, FormParser

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = (MultiPartParser, FormParser)  # Ensure the request is parsed correctly for file uploads

    def create(self, request, *args, **kwargs):
        # Debugging received data
        print("Received data:", request.data)
        print("Received files:", request.FILES)

        product_data = request.data.copy()

        # Extract attribute names and values from request data
        attribute_names = request.data.getlist('attributes[1][attribute_name]')
        attribute_values = request.data.getlist('attributes[1][attribute_value]')

        # Debugging: print the lists of attribute names and values
        print(f"Attribute Names: {attribute_names}")
        print(f"Attribute Values: {attribute_values}")

        # Ensure both lists have the same length
        if len(attribute_names) != len(attribute_values):
            print(f"Mismatch: {len(attribute_names)} != {len(attribute_values)}")
            return Response({
                'error': 'Mismatched attribute names and values',
                'attribute_names': attribute_names,
                'attribute_values': attribute_values
            }, status=status.HTTP_400_BAD_REQUEST)

        # Prepare the structured attributes data
        attributes_data = []
        for i in range(len(attribute_names)):
            attributes_data.append({
                'attribute_name': attribute_names[i],
                'attribute_value': attribute_values[i]
            })

        # Process the product images
        product_images_data = []
        for i in range(len(request.FILES.getlist('productimage[0][image]'))):
            image_field = f'productimage[{i}][image]'
            added_by_field = f'productimage[{i}][added_by]'

            if image_field in request.FILES:
                # Extract the 'added_by' field from the request data
                added_by = request.data.get(added_by_field, None)

                # Debugging: print the 'added_by' for each image
                print(f"Image {i}: {image_field} with added_by: {added_by}")

                # Append image data, ensuring added_by is handled correctly
                product_images_data.append({
                    'image': request.FILES[image_field],
                    'added_by': added_by
                })

        # Debugging: print the final attributes and images data
        print("Processed attributes data:", attributes_data)
        print("Processed product images data:", product_images_data)

        # Set the structured data for the product serializer
        product_data.setlist('attributes', attributes_data)
        product_data.setlist('productimage', product_images_data)

        # Pass the structured data to the serializer
        serializer = self.get_serializer(data=product_data)

        if serializer.is_valid():
            # Save the product instance first
            product = serializer.save()

            # Save each attribute
            if attributes_data:
                for attribute in attributes_data:
                    ProductAttribute.objects.create(product=product, **attribute)

            # Save each image, ensuring we avoid creating extra instances
            if product_images_data:
                for image_data in product_images_data:
                    # Only save product image if there is an image field
                    if image_data.get('image'):
                        ProductImage.objects.create(product=product, **image_data)

            return Response({
                'message': 'Product created successfully!',
                'product': serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            print("Serializer Errors:", serializer.errors)
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
