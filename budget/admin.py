from django.contrib import admin
from django.db.models import Count, Sum

from .models import Budget, Category, BudgetSummary


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


@admin.register(BudgetSummary)
class BudgetSummaryAdmin(admin.ModelAdmin):
    change_list_template = "admin/budget_summary_change_list.html"
    date_hierarchy = "date"
    list_filter = ("category",)

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        try:
            qs = response.context_data["cl"].queryset
        except (AttributeError, KeyError):
            return response

        metrics = {"total": Count("id"), "total_amount": Sum("amount")}
        response.context_data["summary"] = list(
            qs.values("category__name").annotate(**metrics).order_by("-total_amount")
        )
        return response
