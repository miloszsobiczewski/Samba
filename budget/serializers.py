from rest_framework import serializers
from .models import Budget, Category


class BudgetSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )

    class Meta:
        model = Budget
        fields = ("id", "amount", "date", "category", "note")


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "icon", "sign")

