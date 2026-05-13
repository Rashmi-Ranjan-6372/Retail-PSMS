from Backend.masters.serializers.products_category_serializers import ProductCategorySerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from masters.models import Category
from masters.serializers import ProductCategorySerializer

from accounts.permissions import IsAdmin  # your custom permission

# ================= PRODUCT CATEGORY LIST + CREATE ================= #

class ProductCategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [IsAuthenticated, IsAdmin]

# ================= PRODUCT CATEGORY DETAIL ================= #

class ProductCategoryRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [IsAuthenticated, IsAdmin]