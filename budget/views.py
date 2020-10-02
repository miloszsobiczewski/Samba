from django.db.models import Case, DecimalField, F, Sum, Value, When
from django.db.models.functions import (ExtractMonth, ExtractYear, Lower,
                                        Replace)
from django_pivot.pivot import pivot
from rest_framework import viewsets

from budget.models import Budget, Category
from budget.serializers import (BudgetSerializer, CategorySerializer,
                                CategorySummarySerializer,
                                TotalSummarySerializer, YearSummarySerializer)
from budget.services import pivot_mapper as pivot_mapper_service


class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer

    def get_queryset(self):
        """
        Use filtering by year and month or specific date
        """
        year = self.request.query_params.get("year", None)
        month = self.request.query_params.get("month", None)
        date = self.request.query_params.get("date", None)

        if year and month:
            return Budget.objects.filter(date__year=year, date__month=month)
        elif date:
            return Budget.objects.filter(date=date)
        else:
            return Budget.objects.all()


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by()
    serializer_class = CategorySerializer


class CategorySummaryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySummarySerializer

    def get_queryset(self):
        qs = (
            Budget.objects.annotate(
                year=ExtractYear("date"),
                month=ExtractMonth("date"),
                category_name=F("category__name"),
            )
            .values("year", "month", "category_name")
            .annotate(category_sum=Sum("amount"))
        )
        data = Budget.objects.annotate(
            year=ExtractYear("date"),
            month=ExtractMonth("date"),
            category_name=Replace(Lower("category__name"), Value(" "), Value("_")),
        ).values("year", "month", "category_name", "amount")

        pivot_table = pivot(
            data, ["year", "month"], "category_name", "amount", default=0
        )
        pivot_table_json = pivot_mapper_service.to_json(pivot_table)
        return pivot_table_json


class TotalSummaryViewSet(viewsets.ModelViewSet):
    serializer_class = TotalSummarySerializer

    def get_queryset(self):
        return (
            Budget.objects.annotate(
                year=ExtractYear("date"),
                month=ExtractMonth("date"),
                income=Case(
                    When(category__sign=1, then=F("amount")),
                    default=Value(0.00),
                    output_field=DecimalField(),
                ),
                outcome=Case(
                    When(category__sign=-1, then=F("amount")),
                    default=Value(0.00),
                    output_field=DecimalField(),
                ),
            )
            .values("year", "month")
            .annotate(
                sum_income=Sum("income"),
                sum_outcome=Sum("outcome"),
                balance=Sum("income") + Sum("outcome"),
            )
        ).order_by("-year")


class YearSummaryViewSet(viewsets.ModelViewSet):
    serializer_class = YearSummarySerializer

    def get_queryset(self):
        return (
            Budget.objects.annotate(
                year=ExtractYear("date"),
                income=Case(
                    When(category__sign=1, then=F("amount")),
                    default=Value(0.00),
                    output_field=DecimalField(),
                ),
                outcome=Case(
                    When(category__sign=-1, then=F("amount")),
                    default=Value(0.00),
                    output_field=DecimalField(),
                ),
            )
            .values("year")
            .annotate(
                sum_income=Sum("income"),
                sum_outcome=Sum("outcome"),
                avg_income=Sum("income") / 12,
                avg_outcome=Sum("outcome") / 12,
            )
        )
