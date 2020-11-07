from django.urls import path, include
from news import views


app_name = 'news'

urlpatterns = [
    path('', views.NewsListView.as_view(), name='news_list'),
    path('category/<category>/', views.NewsListView.as_view(), name='news_by_category'),
    path('provider/<provider>/', views.NewsListView.as_view(), name='news_by_provider'),
    path('news/<slug:slug>/', views.NewsDetailView.as_view(), name='news_detail'),
    path('search/', views.NewsListView.as_view(), name='search'),
    path('my_home/', views.UserHomeView.as_view(), name='user_home'),
    path('accounts/', include('accounts.urls', namespace='accounts')),
]