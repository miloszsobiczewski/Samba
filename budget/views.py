from rest_framework import viewsets

from .models import Budget, Category
from .serializers import BudgetSerializer, CategorySerializer


class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all().order_by()
    serializer_class = BudgetSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by()
    serializer_class = CategorySerializer
