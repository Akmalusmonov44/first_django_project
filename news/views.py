from django.contrib.admin.utils import reverse_field_path
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.template.defaultfilters import title
from django.template.defaulttags import comment
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from urllib import request

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import FormView, TemplateView
from hitcount.models import HitCount
from hitcount.templatetags.hitcount_tags import get_hit_count
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin
from unicodedata import category

from . import forms
from .models import News, Category, Comment, Contact
from .forms import ContactForm, CommentForm
from .permission import OnlySuperUser


# Create your views here.




def news_detail(request, slug):
    news = get_object_or_404(News, slug=slug, status=News.Status.Published)
    context = {}

    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)



    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits

    comments = news.comments.filter(active=True)
    news_comment = None

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            news_comment = comment_form.save(commit=False)
            news_comment.news = news
            news_comment.save()

            return redirect(news.get_absolute_url())
    else:
        comment_form = CommentForm()

    context = {
        'news': news,
        'comments': comments,
        'news_comment': news_comment,
        'comment_form': comment_form
    }

    return render(request, 'news/news_detail.html', context)


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

class NewsUpdateView(OnlySuperUser,UpdateView):
    model = News
    fields = ('title','body','image', 'category', 'status',)
    template_name = 'crud/news_edit.html'


class NewsDeleteView(OnlySuperUser,DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('home_page')

class NewsCreateView(OnlySuperUser,CreateView):
    model = News
    template_name = 'crud/news_create.html'
    fields = ('title', 'slug','body', 'image', 'category', 'status',)


@login_required
@user_passes_test(lambda u:u.is_superuser)
def admin_page_view(request):
    admin_users = User.objects.all()
    context = {
        'admin_users':admin_users
    }
    return render(request, 'news/admin_page.html', context)


class SearchResultlistView(ListView):
    model = News
    template_name = 'news/search_result.html'
    context_object_name = 'barcha_yangiliklar'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query )

        )


