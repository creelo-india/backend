from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'description', 'children', 'created_at']
        read_only_fields = ['children']

    def get_children(self, obj):
        children = obj.children.all()
        return CategorySerializer(children, many=True).data
