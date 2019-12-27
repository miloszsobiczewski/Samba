import json
import datetime
from pathlib import Path

from django.http import HttpResponseRedirect

from features.downloaders.samba import SambaSynchro
from .models import Connection
from budget.models import Category, Budget


def download(request, id):
    config = json.loads(Connection.objects.get(pk=id).config)
    samba = SambaSynchro(config)

    files_list = samba.listFiles()
    samba.download()

    for file in files_list:
        year = int(f"20{file[:2]}")
        month = int(f"{file[3:5]}")
        queryset = Budget.objects.filter(date__year=year, date__month=month)
        if queryset:
            queryset.delete()
        for instance in json.loads(Path(f"data/{file}").read_text()):
            category = instance["category"]
            category_obj, _ = Category.objects.get_or_create(name=category)
            Budget.objects.create(
                amount=instance["amount"],
                date=datetime.datetime.strptime(instance["date"], "%d.%m.%Y"),
                note=instance["note"],
                category=category_obj,
            )
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
