from django.contrib import admin
from .models import News, Category, Comment, Contact


# Register your models here.

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug','publish_time', 'status')
    list_filter = ('status','created_time','publish_time')
    prepopulated_fields = {'slug':('title',)}
    search_fields = ['title','body']
    actions = ['display_comments', 'activate_comments']
    date_hierarchy = 'publish_time'
    ordering = ('-publish_time','status')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'body', 'created_time', 'active']
    list_filter = ['active', 'created_time']
    search_fields = ['user', 'body']
    actions = ['disable_comments', 'activate_comments']

    def disable_comments(self, request, queryset):
        queryset.update(active=False)

    def activate_comments(self, request, queryset):
        queryset.update(active=True)


admin.site.register(Contact)





