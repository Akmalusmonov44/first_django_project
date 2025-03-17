from nturl2path import pathname2url

from django.urls import path
from .views import news_detail, indexView, ContactPageView, \
    LocalNewsView, ForeignNewsView, TexnologyNewsView, SportNewsView


urlpatterns = [
    path('', indexView, name='home_page'),
    path('news/<slug:slug>/', news_detail, name='news_details_page'),
    path('contact/', ContactPageView.as_view(), name='contact'),
    path('local-news/', LocalNewsView.as_view(), name='local_page'),
    path('foreign/news', ForeignNewsView.as_view(), name='foreign_page' ),
    path('texnology/', TexnologyNewsView.as_view(), name='texnology_page' ),
    path('sport/', SportNewsView.as_view(), name='sport_page')
]
