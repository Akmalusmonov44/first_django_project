from django.contrib import admin
from .models import News, Category, Comment, Contact


# Register your models here.

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug','publish_time', 'status')
    list_filter = ('status','created_time','publish_time')
    prepopulated_fields = {'slug':('title',)}
    search_fields = ['title','body']
    date_hierarchy = 'publish_time'
    ordering = ('-publish_time','status')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']

admin.site.register(Comment)
admin.site.register(Contact)

