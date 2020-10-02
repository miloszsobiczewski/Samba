from django.contrib import admin
from django.db.models import Count, DateField, DateTimeField, F, Max, Min, Sum
from django.db.models.functions import Trunc
from django.utils.safestring import mark_safe

from .models import (Budget, BudgetSummary, Category, QuarterTotal,
                     QuarterTotalSummary, Tower)


@admin.register(Budget)
class ActualisationAdmin(admin.ModelAdmin):
    search_fields = ["category__name", "date"]
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


def make_planned(modeladmin, request, queryset):
    queryset.update(status="planned", percentage=30)


def make_set(modeladmin, request, queryset):
    queryset.update(status="set", percentage=40)


def make_in_progress(modeladmin, request, queryset):
    queryset.update(status="in_progress", percentage=50)


def make_finished(modeladmin, request, queryset):
    queryset.update(status="finished", percentage=100)


def make_hold(modeladmin, request, queryset):
    queryset.update(status="finished")


make_planned.short_description = "Mark selected tasks as planned"
make_set.short_description = "Mark selected tasks as set"
make_in_progress.short_description = "Mark selected tasks as in progress"
make_hold.short_description = "Mark selected tasks as on hold"
make_finished.short_description = "Mark selected tasks as finished"


@admin.register(Tower)
class TowerAdmin(admin.ModelAdmin):
    model = Tower
    ordering = ["-added_date", "-id"]
    list_display = [
        "id",
        "level",
        "task",
        "added_date",
        "days_last",
        "plan_material_cost",
        "plan_work_cost",
        "real_cost",
        "status",
        "percent",
    ]
    change_list_template = "admin/tower_change_list.html"
    actions = [make_finished, make_hold, make_in_progress, make_planned, make_set]

    def plan_material_cost(self, obj):
        return obj.plan_amount_material

    def plan_work_cost(self, obj):
        return obj.plan_amount_work

    def real_cost(self, obj):
        return obj.real_amount

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        try:
            qs = response.context_data["cl"].queryset
        except (AttributeError, KeyError):
            return response
        metrics = {"total": Sum("real_amount")}
        total = "{:0,.2f}".format(float(qs.aggregate(**metrics)["total"]))
        response.context_data["summary"] = {"total": total}
        return response

    def percent(self, obj):
        per = obj.percentage
        done = """
        <svg width="%s" height="15"><rect width="%s" height="15" style="fill:%s" /></svg>
        """
        left = """
        <svg width="%s" height="15"><rect width="%s" height="15" style="fill:gray" /></svg>
        """
        colors = [
            done % (per * 2, per * 2, obj.color),
            left % ((100 - per) * 2, (100 - per) * 2),
        ]
        return mark_safe("".join(colors))


@admin.register(QuarterTotal)
class QuarterTotalAdmin(admin.ModelAdmin):
    model = QuarterTotal
    ordering = ["-date_added"]
    list_display = [
        "year",
        "quarter",
        "total_amount",
        "amount_kejt",
        "amount_mewash",
        "amount_safe",
        "amount_gbp",
        "amount_usd",
        "date_added",
        "note",
    ]


@admin.register(QuarterTotalSummary)
class QuarterTotalSummaryAdmin(admin.ModelAdmin):
    change_list_template = "admin/quarter_total_summary_change_list.html"

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        try:
            qs = response.context_data["cl"].queryset
        except (AttributeError, KeyError):
            return response

        # table
        response.context_data["summary"] = list(
            qs.values("year", "quarter").annotate(
                total_amount=F("amount_kejt") + F("amount_mewash") + F("amount_safe")
            )
        )

        # chart
        summary_over_time = (
            qs.annotate(period=F("date_added"))
            .values("period", "year", "quarter")
            .annotate(total=F("amount_kejt") + F("amount_mewash") + F("amount_safe"))
            .order_by("period")
        )
        summary_range = summary_over_time.aggregate(low=Min("total"), high=Max("total"))
        high = summary_range.get("high", 0)
        # low = summary_range.get("low", 0)
        low = 0
        response.context_data["summary_over_time"] = [
            {
                "period": x["period"],
                "year": x["year"],
                "quarter": x["quarter"],
                "total": x["total"] or 0,
                "pct": ((x["total"] or 0) - low) / (high - low) * 100
                if high > low
                else 0,
            }
            for x in summary_over_time
        ]

        return response
