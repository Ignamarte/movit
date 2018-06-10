from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from pages.views import Home

urlpatterns = [
    url(r'^gestion/', admin.site.urls),
    url(r'^$', Home.as_view(), name="home"),
    url(r'^pages/', include('pages.urls', namespace="pages")),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #For dev purpose only
