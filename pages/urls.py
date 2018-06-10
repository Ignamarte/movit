from django.conf.urls import url, include
from pages.views import ProductionList, VideoView, TeamView, ArticleView, PageView, ArticleDetailView, credit

urlpatterns = [
    url(r'^prod/(?P<pk>\d+)$', ProductionList.as_view(), name="prod"),
    url(r'^prod/(?P<pk>\d+)/(?P<page>\d+)$', ProductionList.as_view(), name="prod-page"),
    url(r'^video/(?P<pk>\d+)$', VideoView.as_view(), name="video"),
    url(r'^blog-detail/(?P<pk>\d+)$', ArticleDetailView.as_view(), name="blog_detail"),
    url(r'^blog/$', ArticleView.as_view(), name="blog"),
    url(r'^page/(?P<pk>\d+)$', PageView.as_view(), name="page"),
    url(r'^team/(?P<pk>\d+)$', TeamView.as_view(), name="specific-team"),
    url(r'^team/$', TeamView.as_view(), name="team"),
    url(r'^credit/$', credit , name="credit"),
]
