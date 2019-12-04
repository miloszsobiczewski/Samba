from django.conf.urls import url

from . import views as features_views

app_name = "features"


urlpatterns = [
    url(r"^download/(?P<id>[-\w]+)/$", features_views.download, name="download")
]
