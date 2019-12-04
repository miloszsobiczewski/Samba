from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import Connection


@admin.register(Connection)
class ActualisationAdmin(admin.ModelAdmin):
    model = Connection
    ordering = ["-name"]
    list_display = ["name", "user", "password", "download"]

    def download(self, obj):
        return format_html(
            '<a class="button" href="{}">Download</a>&nbsp;',
            reverse("features:download", args=[obj.pk]),
        )
