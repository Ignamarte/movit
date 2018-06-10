from django.http import HttpResponse, Http404
from django.template import Context, loader
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.views.generic import View, DetailView, ListView
from movit.settings import LIMIT_YEARS_DISPLAY, LIMIT_YEARS, FACEBOOK_PAGE, GARBAGE_URL, VIDEO_URL, VIDEO_PER_PAGES

from pages.models import Showcase, Partnership, Production, Video, Team, Member, News, Page

class Home(View):

    template_name = 'pages/home.html'

    def get(self, request, *args, **kwargs):
        partners = Partnership.objects.all().order_by('order')
        slides = Showcase.objects.all()

        partnersWithDelay = []
        for i in range(len(partners)):
            partnersWithDelay += [(partners[i], 0.3+i*0.2)]

        context = {
            'partners': partnersWithDelay,
            'slides': slides,
            'fb_link': FACEBOOK_PAGE,
            'video_link' : VIDEO_URL,
        }
        context = complete_context(context)
        return render(request, self.template_name, context)


class ProductionList(DetailView):

    template_name = 'pages/list_vids.html'
    model = Production
    context_object_name = 'prod'

    def get_context_data(self, **kwargs):
        page = self.kwargs.get('page', None)
        if page:
            page = int(page)
        else:
            page = 1
        context = super(ProductionList, self).get_context_data(**kwargs)
        videos = Video.objects.filter(production=self.kwargs['pk']).order_by('-year','-date')
        if videos:
            p = Paginator(videos, VIDEO_PER_PAGES)
            try :
                videos = p.page(page)
            except EmptyPage:
                raise Http404
            year = videos[0].year
            sorted_videos = []
            singleYearVideos = []
            for video in videos:
                if video.year != year:
                    sorted_videos.append(singleYearVideos)
                    singleYearVideos = [video]
                    year = video.year
                else:
                    singleYearVideos.append(video)
            sorted_videos.append(singleYearVideos)
            context["sorted"] = sorted_videos
            if videos.has_next():
                context["has_next"] = True
                context["next"] = videos.next_page_number()
            if videos.has_previous():
                context["has_previous"] = True
                context["previous"] = videos.previous_page_number()

        else:
            context["sorted"] = []
        context = complete_context(context)
        return context


class VideoView(DetailView):

    template_name = 'pages/video.html'
    model = Video
    context_object_name = 'video'

    def get_object(self, queryset=None):
        obj = super(DetailView, self).get_object(queryset=queryset)
        obj.count = obj.count +1
        obj.save()
        return(obj)

    def get_context_data(self, **kwargs):
        context = super(VideoView, self).get_context_data(**kwargs)
        context = complete_context(context)
        return context

class TeamView(View):

    template_name = "pages/team.html"

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk', None)
        if pk:
            team = get_object_or_404(Team, year=pk)
        else:
            team = Team.objects.all().order_by('-year')
            if team: team = team.first()
        members = Member.objects.filter(team=team.pk, is_prez=False)
        prezs = Member.objects.filter(team=team.pk, is_prez=True)
        years = self.get_years()
        context = {
            'members': members,
            'prezs': prezs,
            'team': team,
            'years': years,
        }
        context = complete_context(context)
        return render(request, self.template_name, context)

    def get_years(self):
        teams = Team.objects.all().order_by('-year')
        years = [team.year for team in teams]
        if LIMIT_YEARS_DISPLAY and len(years) > LIMIT_YEARS:
            years[:LIMIT_YEARS]
        return years

class ArticleView(ListView):

    template_name = "pages/article.html"
    model = News
    context_object_name = "news"
    paginate_by = 4
    ordering = ['-date']

    def get_context_data(self, **kwargs):
        context = super(ArticleView, self).get_context_data(**kwargs)
        context = complete_context(context)
        return context

class ArticleDetailView(DetailView):

    template_name = "pages/article_detail.html"
    model = News
    context_object_name = "news"

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context = complete_context(context)
        return context

class PageView(DetailView):

    template_name = "pages/page.html"
    model = Page
    context_object_name = "page"

    def get_context_data(self, **kwargs):
        context = super(PageView, self).get_context_data(**kwargs)
        context = complete_context(context)
        return context

def credit(request):
    template = loader.get_template("pages/credit.html")
    return HttpResponse(template.render)


def complete_context(context):
    """
    Small function that returns provided context with additional content
    """
    context["productions"] = Production.objects.all().order_by('order')
    context["pages"] = Page.objects.all()
    context["garbage_url"] = GARBAGE_URL
    return context
