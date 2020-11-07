from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
import datetime

from news.models import News, NewsProvider, NewsCategory


# Create your views here.
class NewsListView(ListView):
    template_name = "news/latest_news_list.html"
    context_object_name = "news_list"
    paginate_by = 10

    def get_queryset(self):
        if self.kwargs.get("provider"):
            queryset = News.objects.filter(provider__slug=self.kwargs["provider"])
        elif self.kwargs.get("category"):
            queryset = News.objects.filter(category__slug=self.kwargs["category"])
        elif self.request.GET.getlist("category"):
            queryset = News.objects.filter(category__slug__in=self.request.GET.getlist("category"))

            if self.request.GET.getlist("provider"):
                queryset = queryset.filter(provider__slug__in=self.request.GET.getlist("provider"))
            
            if self.request.GET.getlist("phrase"):
                queryset = queryset.filter(
                    Q(headline__icontains=self.request.GET.get("phrase")) |
                    Q(story_excerpt__icontains=self.request.GET.get("phrase")) |
                    Q(story_content__icontains=self.request.GET.get("phrase"))
                )
        elif self.request.GET.getlist("provider"):
            queryset = News.objects.filter(provider__slug__in=self.request.GET.getlist("provider"))
            
            if self.request.GET.getlist("phrase"):
                queryset = queryset.filter(
                    Q(headline__icontains=self.request.GET.get("phrase")) |
                    Q(story_excerpt__icontains=self.request.GET.get("phrase")) |
                    Q(story_content__icontains=self.request.GET.get("phrase"))
                )
        elif self.request.GET.getlist("phrase"):
            queryset = News.objects.filter(
                Q(headline__icontains=self.request.GET.get("phrase")) |
                Q(story_excerpt__icontains=self.request.GET.get("phrase")) |
                Q(story_content__icontains=self.request.GET.get("phrase"))
            )
        else:
            # get news items from last 24 hours only
            start = datetime.date.today()
            end = start + datetime.timedelta(days=1)
            queryset = News.objects.filter(created_on__range=(start, end))
        return queryset


class UserHomeView(LoginRequiredMixin, ListView):
    template_name = "news/latest_news_list.html"
    context_object_name = "news_list"
    paginate_by = 10

    def get_queryset(self):
        start = datetime.date.today()
        end = start + datetime.timedelta(days=1)

        if self.request.user.preferences.category:
            user_categories = [self.request.user.preferences.category.slug]
        else:
            user_categories = list(NewsCategory.objects.all())
            for index, category in enumerate(user_categories):
                user_categories[index] = category.slug

        if self.request.user.preferences.provider:
            user_providers = [self.request.user.preferences.provider.slug]
        else:
            user_providers = list(NewsProvider.objects.all())
            for index, provider in enumerate(user_providers):
                user_providers[index] = provider.slug

        queryset = News.objects.filter(
                                # created_on__range=(start, end),
                                category__slug__in=user_categories,
                                provider__slug__in=user_providers)
        return queryset


class NewsDetailView(DetailView):
    model = News
    template_name = "news/news_detail.html"
    context_object_name = "news_detail"
    slug_url_kwarg = "slug"
    slug_field = "slug"
