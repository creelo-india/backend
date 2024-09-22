# urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet

# Initialize the router
router = DefaultRouter()

# Register the CategoryViewSet with the router
router.register(r'categories', CategoryViewSet)

# Define the URL patterns
urlpatterns = [
    path('', include(router.urls)),  # Include the router URLs
]
