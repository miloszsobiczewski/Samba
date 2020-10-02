from rest_framework import serializers

from .models import Budget, Category


class BudgetSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Budget
        fields = ("id", "amount", "date", "category", "note")


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "icon", "sign")


class CategorySummarySerializer(serializers.Serializer):
    year = serializers.IntegerField()
    month = serializers.IntegerField()
    data = serializers.JSONField()


class YearSummarySerializer(serializers.Serializer):
    year = serializers.IntegerField()
    sum_income = serializers.DecimalField(max_digits=8, decimal_places=2)
    sum_outcome = serializers.DecimalField(max_digits=8, decimal_places=2)
    avg_income = serializers.DecimalField(max_digits=8, decimal_places=2)
    avg_outcome = serializers.DecimalField(max_digits=8, decimal_places=2)


class TotalSummarySerializer(serializers.Serializer):
    year = serializers.IntegerField()
    month = serializers.IntegerField()
    sum_income = serializers.DecimalField(max_digits=8, decimal_places=2)
    sum_outcome = serializers.DecimalField(max_digits=8, decimal_places=2)
    balance = serializers.DecimalField(max_digits=8, decimal_places=2)
