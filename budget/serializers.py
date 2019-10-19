from rest_framework import serializers
from .models import Budget, Category


class BudgetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Budget
        fields = "__all__"


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

