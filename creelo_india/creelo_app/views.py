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
from rest_framework.response import Response
from rest_framework import status
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        # Preprocess attributes
        attributes_data = []
        i = 0
        while f'attributes[{i}][attribute_name]' in request.data:
            attributes_data.append({
                'attribute_name': request.data.get(f'attributes[{i}][attribute_name]'),
                'attribute_value': request.data.get(f'attributes[{i}][attribute_value]')
            })
            i += 1

        # Preprocess product images
        product_images_data = []
        i = 0
        while f'product_images[{i}][image]' in request.FILES:
            product_images_data.append({
                'image': request.FILES[f'product_images[{i}][image]'],
                'added_by': request.data.get(f'product_images[{i}][added_by]')
            })
            i += 1

        # Prepare main product data
        product_data = {key: request.data[key] for key in request.data if not key.startswith('attributes') and not key.startswith('product_images')}

        # Add attributes and images to the main data
        product_data['attributes'] = attributes_data
        product_data['product_images'] = product_images_data

        # Use the serializer to validate and save the data
        serializer = self.get_serializer(data=product_data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Product created successfully!', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

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
    """
    Handles adding, increasing, reducing, or deleting items in the cart.
    """
    try:
        product_id = request.data.get('product_id')
        action = request.data.get('action')  # "add", "increase", "reduce", "delete"
        quantity = request.data.get('quantity', 1)

        # Validate inputs
        if not product_id or not action:
            return Response({"error": "Product ID and action are required."}, status=status.HTTP_400_BAD_REQUEST)

        product = Product.objects.get(id=product_id)
        cart = get_user_cart(request.user)

        # Fetch or create the cart item
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if action == "add":
            if created:  # New item in the cart
                cart_item.quantity = quantity
            else:  # Update quantity of an existing item
                cart_item.quantity += quantity
            cart_item.save()
            return Response({"message": "Product added to cart."}, status=status.HTTP_201_CREATED)

        elif action == "increase":
            cart_item.quantity += quantity
            cart_item.save()
            return Response({"message": "Product quantity increased."}, status=status.HTTP_200_OK)

        elif action == "reduce":
            if cart_item.quantity > quantity:
                cart_item.quantity -= quantity
                cart_item.save()
                return Response({"message": "Product quantity reduced."}, status=status.HTTP_200_OK)
            else:  # If quantity becomes 0 or less, remove the item
                cart_item.delete()
                return Response({"message": "Product removed from cart."}, status=status.HTTP_200_OK)

        elif action == "delete":
            cart_item.delete()
            return Response({"message": "Product removed from cart."}, status=status.HTTP_200_OK)

        else:
            return Response({"error": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)

    except Product.DoesNotExist:
        return Response({"error": "Product not found."}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_cart(request):
    cart = get_user_cart(request.user)
    serializer = CartSerializer(cart)
    return Response(serializer.data)     




class GetProductList(APIView):
    def get(self, request, *args, **kwargs):
        try:
            products = Product.objects.all()
            serializer = GetProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

