from django.views.generic import ListView
from urllib import request

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import FormView, TemplateView
from unicodedata import category

from . import forms
from .models import News, Category, Comment, Contact
from .forms import ContactForm
# Create your views here.


def news_detail(request, slug ):
    news = get_object_or_404(News, slug=slug, status=News.Status.Published)
    context = {
        'news': news
    }
    return render(request, 'news/news_detail.html',context)



def indexView(request):
    categories = Category.objects.all()
    news_list = News.published.all().order_by('-publish_time')[:4]
    texnologiya = News.published.all().filter(category__name='Texnologiya').order_by('-publish_time')[:6]
    xorijiy_xabarlar = News.published.all().filter(category__name='Xorij').order_by('-publish_time')[:6]
    mahalliy_xabarlar = News.published.all().filter(category__name='Home').order_by('-publish_time')[:6]
    sport_xabarlari = News.published.all().filter(category__name='Sport').order_by('-publish_time')[:6]
    context = {
        'mahalliy_xabarlar': mahalliy_xabarlar,
        'news_list': news_list,
        'categories': categories,
        'xorijiy_xabarlar':xorijiy_xabarlar,
        'texnologiya':texnologiya,
        'sport_xabarlari':sport_xabarlari
    }

    return render(request, 'news/index.html', context)


# class HomePageView(ListView):
#     model = News
#     template_name = 'news/index.html'
#     context_object_name = 'news'
#
#     def get_context_data(self, ** kwargs):
#         context = super().get_context_data(** kwargs)
#         context['categories'] = self.model.objects.all()
#         context['news_list'] = News.published.all().order_by('-publish_time')[:5]
#         context['local_main'] = News.published.filter(category__name='Blog').order_by('-publish_time')[:1]
#         context['local_news'] = News.published.all().filter(category__name='Blog').order_by('-publish_time')[:6]
#         return context
















class ContactPageView(TemplateView):
    template_name = 'news/contact.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {
            'form': form
        }
        return render(request, 'news/contact.html', context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return HttpResponseRedirect('')
        context = {
            'form': form
        }
        return render(request, 'news/contact.html', context)







class LocalNewsView(ListView):
    
    model = News
    template_name = 'news/local.html'
    context_object_name = 'local_news'


    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Home')
        return news

class ForeignNewsView(ListView):
    model = News
    template_name = 'news/foreign.html'
    context_object_name = 'foreign_news'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Xorij')
        return news



class TexnologyNewsView(ListView):
    model = News
    template_name = 'news/texnology.html'
    context_object_name = 'texnology_news'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Texnologiya')
        return news


class SportNewsView(ListView):
    model = News
    template_name = 'news/sport.html'
    context_object_name = 'sport_news'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Sport')
        return news

