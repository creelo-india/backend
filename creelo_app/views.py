from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Product,ProductAttribute,ProductImage
from .serializers import ProductSerializer

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
