from rest_framework import viewsets, generics

from .models import Budget, Category
from .serializers import BudgetSerializer, CategorySerializer


class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer

    def get_queryset(self):
        """
        Use filtering by year and month or specific date
        """
        year = self.request.query_params.get('year', None)
        month = self.request.query_params.get('month', None)
        date = self.request.query_params.get('date', None)

        if year and month:
            return Budget.objects.filter(date__year=year, date__month=month)
        elif date:
            return Budget.objects.filter(date=date)
        else:
            return Budget.objects.all()


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by()
    serializer_class = CategorySerializer
