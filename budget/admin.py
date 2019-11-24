from django.contrib import admin

from .models import Budget, Category


@admin.register(Budget)
class ActualisationAdmin(admin.ModelAdmin):
    model = Budget
    ordering = ["-date"]
    list_display = ["date", "amount", "note", "category"]


@admin.register(Category)
class ActualisationAdmin(admin.ModelAdmin):
    model = Category
    ordering = ["name"]
    list_display = ["name", "icon", "sign"]
